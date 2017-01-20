from PySide.QtGui import QApplication,QWidget,QVBoxLayout,QPushButton

from  PySide.QtWebKit import QWebView
# Create an application
app = QApplication([])

# And a window
win = QWidget()
win.setWindowTitle('QWebView Interactive Demo')

# And give it a layout
layout = QVBoxLayout()
win.setLayout(layout)

# Create and fill a QWebView
view = QWebView()
view.setHtml('''
<!DOCTYPE html>
<html>
  <head>
    <style>
       #map {
        height: 400px;
        width: 100%;
       }
    </style>
  </head>
  <body>
    <h3>My Google Maps Demo</h3>
    <div id="map"></div>
    <script>
      function initMap() {
        var uluru = {lat: -25.363, lng: 131.044};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 4,
          center: uluru
        });
        var marker = new google.maps.Marker({
          position: uluru,
          map: map
        });
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAFOKhKZQElJM0Fh-4VhDrFR6epdHmePfs&callback=initMap">
    </script>
  </body>
</html>
''')


# Add the QWebView and button to the layout
layout.addWidget(view)


# Show the window and run the app
win.show()
app.exec_()