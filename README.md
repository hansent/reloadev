### reloadev

to run example:

 * start reloadev web socket server monitoring example directory
 * go into _example_ directory
 * start a simple http server
 * now visit http://localhost:8000 
 * it will reload the page if you edit and save any of the files in _example_

```bash
        ./reloadev example &
        cd example
        python -m SimpleHTTPServer
```

