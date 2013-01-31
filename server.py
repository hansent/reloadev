import tornado
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.autoreload
import watchdog.observers
import watchdog.events


class ClientScriptHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/javascript')
        self.render('reloadev.js')


class SocketConnection(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.socket_connections.append(self)

    def on_close(self):
        self.application.socket_connections.remove(self)

    def notify(self):
        self.write_message('update')



class FSEventHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, callback=None):
        self.callback = callback

    def dispatch(self, fs_event):
        self.callback(fs_event)


class ReloadevApp(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(ReloadevApp, self).__init__(*args, **kwargs)
        self.socket_connections = []

        self.fs_observer = watchdog.observers.Observer()
        self.fs_observer.start()

    def watch_folder(self, path, recursive=True):
        fs_event_handler = FSEventHandler(self.on_fs_event)
        self.fs_observer.schedule(fs_event_handler, path, recursive)

    def on_fs_event(self, fs_event):
        tornado.ioloop.IOLoop.instance().add_callback(self.notify_clients)

    def notify_clients(self):
        for c in self.socket_connections:
            c.notify()


application = ReloadevApp([
    (r'/socket', SocketConnection),
    (r'/reloadev\.js', ClientScriptHandler),
], debug=True)


if __name__ == '__main__':
    import sys
    watch_path = "."
    if len(sys.argv) == 2:
        watch_path = sys.argv[1]

    application.watch_folder(watch_path)
    application.listen(9999)

    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()

    application.fs_observer.stop()
    application.fs_observer.join()

