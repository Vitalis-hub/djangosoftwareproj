var origin = null
var destination = null
var btnContainer = null
var btns = null
var originManuallyInput = true

var defaultBounds = new google.maps.LatLngBounds(
  new google.maps.LatLng(35.653791, -97.472436),
  new google.maps.LatLng(35.6534127, -97.470890));
function setOriginVar(){
    origin = $('#origin-search-id').search('get value');
}

function setDestinationVar(){
    var input = document.getElementById('destination-search-id');
    var searchBox = new google.maps.places.SearchBox(input, {
      bounds: defaultBounds
    });

    destination = $('#destination-search-id').search('get value');
}

function setSearchApiSettings() {
    const wheelchair = $('#wheelchairAccessible').is(":checked") === true ? 1 : 0;
    const url = `/search_locations/?q={query}&wheel_chair=${wheelchair}`
//    $('.search').reset();
//    $('#destination-search-id').reset();


    $('#origin-search-id').search({
        apiSettings: {
            url: url
        },
        fields: {
            results : 'results',
            description   : 'description',
            title : 'title'
        },
        minCharacters : 1,
        onSelect: function(result){
            origin = result.address
            return true;
        },
    });
    $('#destination-search-id').search({
        apiSettings: {
            url: url
        },
        fields: {
            results : 'results',
            description   : 'description',
            title : 'title'
        },
        minCharacters : 3,
        onSelect: function(result){
            destination = result.address
            originManuallyInput = false
            return true;
        },
    });
}



// Table

filterSelection("all") // Execute the function and show all columns
function filterSelection(c) {
  var x, i;
  x = document.getElementsByClassName("column");
  if (c == "all") c = "";
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  for (i = 0; i < x.length; i++) {
    w3RemoveClass(x[i], "show");
    if (x[i].className.indexOf(c) > -1) w3AddClass(x[i], "show");
  }
}

// Show filtered elements
function w3AddClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {
      element.className += " " + arr2[i];
    }
  }
}

// Hide elements that are not selected
function w3RemoveClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    while (arr1.indexOf(arr2[i]) > -1) {
      arr1.splice(arr1.indexOf(arr2[i]), 1);
    }
  }
  element.className = arr1.join(" ");
}


window.onload = function(){
    setSearchApiSettings();
    // get location elemets
        $.ajax({
        type: 'GET',
        url: '/get_location_elements/',
        data: {},
        success : function(data){
            if(data.success == 0 ){
                alert(data.message)
            }
            else{
                // Add active class to the current button (highlight it)
                locationContainer = $("#location-element-container").html(data.elements)

                btnContainer = document.getElementById("myBtnContainer");
                btns = btnContainer.getElementsByClassName("btn");
                for (var i = 0; i < btns.length; i++) {
                  btns[i].addEventListener("click", function(){
                    var current = document.getElementsByClassName("active");
                    current[0].className = current[0].className.replace(" active", "");
                    this.className += " active";
                  });
                }
                document.getElementById("show-all-button").click()
                getLocation()
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    })

}

