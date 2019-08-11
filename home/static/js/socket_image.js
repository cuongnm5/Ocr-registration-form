function run() {
    var endpoint = 'ws://' + window.location.host + '/message/';
    var endpoint2 = 'ws://' + window.location.host + '/info/';
    // console.log(window.location.host)
    var socket = new ReconnectingWebSocket(endpoint);
    var socket_info = new ReconnectingWebSocket(endpoint2);

    if (window.File && window.FileReader && window.FileList && window.Blob) {
        document.getElementById('files').addEventListener('change', handleFileSelect, false);
    } else {
        alert('The File APIs are not fully supported in this browser.');
    }

    function handleFileSelect(evt) {
        var f = evt.target.files[0];
        var reader = new FileReader();
        // Closure to capture the file information.
        reader.onload = (function(theFile) {
            return function(e) {
                var binaryData = e.target.result;
                //Converting Binary Data to base 64
                var base64String = window.btoa(binaryData);
                //showing file converted to base64
                // document.getElementById('base64').value = base64String;
                socket.send(JSON.stringify({"imgstring": base64String }));
                alert('File converted to base64 successfuly!\nCheck in Textarea');
            };
        })(f);
        // Read in the image file as a data URL.
        reader.readAsBinaryString(f);
    };

    socket.onmessage = function(e) {
        console.log(e);
        var responseData = JSON.parse(e.data);
        var file_name = 'data:image/png;base64,' + responseData.base64;
        $('#images').append($('<div class="clickable_img" onclick="show_img_details(\'' +
            file_name + ' \')"> <img width = \"100\" class="img-fluid img-thumbnail" alt=\"Avatar\"src=\"data:image/png; base64, ' +
            responseData.base64 + '\
                    "></div>'));
        var text_data = JSON.parse(responseData.Question);
        console.log(text_data);
        var i = 0;
        for (ans in text_data) {
            i++;
            $('#result').append($('<div class="form-group"><h3><div class="list-group-item "><label for="first_name"><h4>' +
                text_data[ans]['text'] + '</h4></label><input style="background-color:rgb(63, 54, 78) " type="text" class="form-control" name="input' + String(i) + '"id="first_name"></div></h3></div>'));
            console.log(text_data[ans]['text']);
        }
        $('#result').append($('<div class="form-group "><div class="form-group "><div class="col-xs-12 "><button class="btn btn-lg btn-success " ><i class="glyphicon glyphicon-ok-sign "></i> Save</button></div></div></div>'));



    };

    $('#result').submit(function() {
        // get all the inputs into an array.
        var $inputs = $('#result :input');
    
        // not sure if you wanted this, but I thought I'd add it.
        // get an associative array of just the values.
        var values = {}; //object contant personal information
        $inputs.each(function() {
            values[this.name] = $(this).val();
        });
        console.log(values);
        socket_info.send(JSON.stringify({'infomation': JSON.stringify(values)}));
        
        return false;
    });

    socket_info.onmessage = function(e){
        console.log(e.data);
    }


};

run();