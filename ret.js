ymaps.ready(function () {

    var map = new ymaps.Map('map', {
        center: [55.79, 37.64],
        zoom: 10,
        controls: ['zoomControl']
    }),
    objectManager = new ymaps.ObjectManager();

    $.getJSON('/polyline.json')
        .done(function (geoJson) {
            objectManager.add(geoJson);
            map.geoObjects.add(objectManager);
        });
});
