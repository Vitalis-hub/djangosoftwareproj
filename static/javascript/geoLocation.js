

function getLocation() {
    function showPosition(position) {
        $.ajax({
            type: 'GET',
            url: '/get_address/',
            data: {
                address: `${position.coords.latitude},${position.coords.longitude}`,
            },
            success : function(data){
                if(data.success == 0 ){
                    alert(data.message)
                }
                else{
                    $('#origin-search-id').search('set value', data.address);
                    originManuallyInput = false
                    origin = data.address
                    setSearchApiSettings()
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
    }
    if ( navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser. Please type in address")
    }
}

function loadMapDirectionElements() {
    if (originManuallyInput == true) {
        origin = $('#origin-search-id').search('get value');
    }
    $.ajax({
        type: 'GET',
        url: '/get_directions/',
        data: {
            origin: origin,
            destination: destination,
        },
        success : function(data){
            if(data.success == 0 ){
                alert(data.message)
            }
            else{
                var htmlString = ''
                data.directions.forEach((element) => {
                    htmlString = htmlString + element + '<br>'
                });
                $('#map-modal-div').html(htmlString);
                $('#map-modal').modal('show');
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    })
}

function loadEntranceElements(locationID) {
    $.ajax({
        type: 'GET',
        url: `/get_entrances/${locationID}`,
        data: null,
        success : function(data){
            if(data.success == 0 ){
                alert(data.message)
            }
            else{
                $('#entrance-modal-div').html(data.element_string);
                $('#entrance-modal').modal('show');
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    })
}

function goToLocation(data){
    destination = data.address
    $('#destination-search-id').search('set value', data.title);
    loadMapDirectionElements()
}
