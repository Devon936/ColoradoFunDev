function search_and_map_init() {
        var info = JSON.parse('<%- JSON.stringify(events) %>');
        var debugWindow = document.getElementById('debugWindow');
        //debugWindow.innerHTML += info;
        
        var mapOptions = {
            zoom: 7,
            center: {lat: 39.4, lng: -105.0},
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            streetViewControl: false,
            mapTypeControl: false
        };

        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
        var eventList = document.getElementById('eventList');

        Date.prototype.monthNames = [
        "Jan", "Feb", "Mar",
        "Apr", "May", "Jun",
        "Jul", "Aug", "Sep",
        "Oct", "Nov", "Dec"
        ];

        Date.prototype.getMonthName = function() {
            return this.monthNames[this.getMonth()];
        };

        var markers = info.map(function(data, i){
          var date = new Date(data['date']);
          // CREATE LIST ELEMENTS
          eventList.innerHTML += 
           '<tr class="event" onclick="eventSelected(this);">'+
            '<td class = "DateCol">'+
              '<p class="day">'+date.getDate()+'</p>'+
              '<p class="month">'+date.getMonthName()+'</p>'+ 
            '</td>'+
            '<td class = "TitleCol">'+data['title']+'</td>'+
            '<td class = "DescriptionCol">Fun Stuff</td>'+
            '<td class = "LocationCol">'+data['city']+'</td>'+
          '</tr>';

          // CREATE MAP MARKERS
          var marker =  new google.maps.Marker({
            position: {lat: data['lat'], lng: data['lng']},
            map: map
          });
          var infowindow = new google.maps.InfoWindow({
            content: data['title']
          });
          marker.addListener('click',function() {
            infowindow.open(map, marker);
          });
          
          return marker;
      
        });
        
      }