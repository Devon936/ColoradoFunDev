 document.getElementById("header").innerHTML =
 '<ul class="nav nav-pills pull-right">'+
  '<li><a href="/">Home</a></li>'+
  '<li><a href="/about">About</a></li>'+
  '<li>'+
	'<div class="dropdown">'+
	  '<button class="dropbtn">Summer</button>'+
	  '<div class="dropdown-content">'+
	  	'<a href="/stateparks?test=value">State Parks</a>'+
	    '<a href="/horseback">Horseback Rides</a>'+
	    '<a href="/winecountry">Wine Country</a>'+
	    '<a href="/golfcourse">Golf Courses</a>'+
	    '<a href="/hotsprings">Hot Springs</a>'+
	  '</div>'+
	'</div>'+
  '</li>'+
  '<li><a href="/map">Things To Do</a></li>'+
  '<li><a href="/user">Log In</a></li>'+
 '</ul>'+
 '<img src="/images/logo.jpg">';

document.getElementById("ad_area1").innerHTML =
	'<div id="sidebar-wrapper" style="border-style: solid; padding: 10px; margin: 10px">'+
	'<span>Ad area 1</span>'+
	'</div>';
document.getElementById("ad_area2").innerHTML =
	'<div id="sidebar-wrapper" style="border-style: solid; padding: 10px; margin: 10px">'+
	'<span>Ad area 2</span>'+
	'</div>';

 document.getElementById("footer").innerHTML =
 '<p>&copy; ColoradoFun - 2018</p>';
 
$('.nav a').each(function() {
	var url = String(location.href.split("/").slice(-1));
	var link = this.href.split("/").slice(-1);
	if (url == link){
		$(this).addClass('active');
	}
});

$(function() {
	$( ".datepicker" ).datepicker({
		dateFormat: 'yy-mm-dd',
		onSelect: function(selected, evnt) {
			activeSearch();
		}
	});
});

$('#categoryList').tree({
  dataSource: [
  	{text: 'Categories', children: [
	    {text: 'spring', children: [
	      {text: 'family'},
	      {text: 'music'}
	    ]},
	    {text: 'summer', children: [
	      {text: 'water', children: [
	      	{text: 'swimming'},
	      	{text: 'snorkel'}
	      ]},
	      {text: 'sun'}
	    ]},
	    {text: 'fall', children: [
	      {text: 'hikes'},
	      {text: 'art'}
	    ]},
	    {text: 'winter', children: [
	      {text: 'ski'},
	      {text: 'shopping'}
	    ]}
	]}
  ]
});

function eventSelected(obj) {
	var table = document.getElementById("eventList");
	var info = [];
	for (var i=0; i<events.length; i++){
		if(events[i]['id']['S'] == obj.id){
			info = events[i];
			break;
		}
	}
	if(obj.className == "selected-event"){
		table.deleteRow(obj.rowIndex+1);
		obj.className = "event";
	}
	else {
    	var NewInfo = '<td colspan=4>'+
    	'<div>'+
    	'<img src="/images/example.jpg" style="width:80px; height:80px; float:left; margin:2px 10px 2px 2px">'+
    	'Full Description. <a href="#">Link to outside source</a> '+
    	info['title']['S']+
    	'Links to similar events.'+
    	'Anything else desired from full event page'+
    	'</div>'+
    	// Suggested Events List
    	'<div id="suggested-events-list" style="border-style: solid; margin: 10px; float: right">Similar Events'+
    	'<ul>'+
			'<li><a Event 1</li>'+
			'<li>Event 2</li>'+
		'</ul></div>'+
		'<a href="/eventinfo?id='+info['id']['S']+'">More Info</a>'+
    	// ad banner
    	'<div>'+
    	'<div id="sidebar-wrapper" style="border-style: solid; margin: 5px 5px 5px 85px; width:500px">'+
			'Ad area'+
		'</div></div></td>';
	    var row = table.insertRow(obj.rowIndex+1);
	    row.innerHTML = NewInfo;
	    obj.className = "selected-event";
	}
}