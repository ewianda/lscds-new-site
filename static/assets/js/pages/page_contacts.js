var ContactPage = function () {

    return {
        
    	//Basic Map
        initMap: function () {
			var map;
			$(document).ready(function(){
			  map = new GMaps({
				div: '#map',
				scrollwheel: false,				
				lat: 43.65941,
				lng: -79.39567
			  });
			  
			  var marker = map.addMarker({
				lat: 43.65941,
				lng: -79.39567,
	            title: 'Company, Inc.'
		       });
			});
        },

        //Panorama Map
        initPanorama: function () {
		    var panorama;
		    $(document).ready(function(){
		      panorama = GMaps.createPanorama({
		        el: '#panorama',
		        lat : 43.65941,
		        lng :-79.39567
		      });
		    });
		}        

    };
}();
