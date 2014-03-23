import SocketServer


class Server(SocketServer.BaseRequestHandler):
    filesystem = {}
    passwords = {
        "admin": "password"
    }

    def send(self, data):
        return self.request.send("{}\n".format(data))

    def recv(self, data=""):
        if data:
            self.request.send(data)
        return self.request.recv(1024).strip()

    def handle(self):
        user = None
        auth = False
        while True:
            if user is None:
                user = self.recv("LOGIN: ")
                continue
            if user and not auth:
                password = self.recv("PASSWORD: ")
                if user in self.passwords and self.passwords[user] == password:
                    auth = True
                    self.send("WELCOME {}".format(user))
                else:
                    user = None
                    self.send("INCORRECT PASSWORD")
                    continue

            response, keepalive = self.shell(self.recv("{}@{}:{}$ ".format(user, "server", "/")), user)
            self.send(response)
            if not keepalive:
                break

    def shell(self, command, user):
        if command == "motd":
            return "{}".format(copyright), True
        if command == "exit":
            return "GOODBYE {}".format(user), False
        return "{} NOT FOUND".format(command), True

    def login(self, username, password):
        pass


class ReusableTCPServer(SocketServer.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    server = ReusableTCPServer(("", 5000), Server)
    server.serve_forever()