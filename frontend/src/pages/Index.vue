<template>
  <q-page class="flex flex-center">
    <div id="viewDiv"></div>
  </q-page>
</template>


<script>
import Map from "@arcgis/core/Map";
import MapView from "@arcgis/core/views/MapView";
import Graphic from "@arcgis/core/Graphic";

export default {
  name: "PageIndex",

  mounted() {
    var map = new Map({
      basemap: "hybrid",
    });

    var view = new MapView({
      center: [59.92380894, 42.54129204],
      container: "viewDiv",
      map: map,
      zoom: 8,
    });

    this.$axios.get("/well_request/0").then((response) => {
      for (let i = 0; i < response.data.length; i++) {
        // First create a point geometry (this is the location of the Titanic)
        var point = {
          type: "point", // autocasts as new Point()
          longitude: response.data[i].x,
          latitude: response.data[i].y,
        };

        // Create a symbol for drawing the point
        var markerSymbol = {
          type: "simple-marker", // autocasts as new SimpleMarkerSymbol()
          color: [226, 119, 40],
          outline: {
            // autocasts as new SimpleLineSymbol()
            color: [255, 255, 255],
            width: 2,
          },
        };
        // Create a graphic and add the geometry and symbol to it
        var pointGraphic = new Graphic({
          geometry: point,
          symbol: markerSymbol,
        });

        // Add the graphics to the view's graphics layer
        view.graphics.addMany([pointGraphic]);
      }
    });
  },
};
</script>

<style lang="stylus" scoped>
#viewDiv {
  height: 600px;
  width: 1200px;
}
</style>
