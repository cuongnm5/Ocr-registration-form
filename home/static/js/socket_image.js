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
                socket.send(JSON.stringify({ "imgstring": base64String }));
                alert('File converted to base64 successfuly!\nCheck in Textarea');
            };
        })(f);
        // Read in the image file as a data URL.
        reader.readAsBinaryString(f);
    };

    $('form').submit(function() {
        // get all the inputs into an array.
        var $inputs = $('#result :input');

        // not sure if you wanted this, but I thought I'd add it.
        // get an associative array of just the values.
        var values = {};
        $inputs.each(function() {
            values[this.name] = $(this).val();
        });
        console.log(values);
    });

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
        socket_info.send(JSON.stringify({ 'infomation': JSON.stringify(values) }));

        return false;
    });

};
run();

{
    /* <img id="scream" width="220" height="277" src="img_the_scream.jpg" alt="The Scream">

    <p>Canvas:</p>
    <canvas id="myCanvas" width="240" height="297" style="border:1px solid #d3d3d3;">
    Your browser does not support the HTML5 canvas tag.
    </canvas>

    <button id="download">download</button>
    <script src="//cdnjs.cloudflare.com/ajax/libs/jspdf/1.3.3/jspdf.min.js"></script>
    <script>
    var canvas = document.getElementById('myCanvas');

    // draw a blue cloud
    window.onload = function() {
      var c = document.getElementById("myCanvas");
      var ctx = c.getContext("2d");
      var img = document.getElementById("scream");
      ctx.drawImage(img, 10, 10);
    }

    download.addEventListener("click", function() {
      // only jpeg is supported by jsPDF
      var imgData = canvas.toDataURL("image/jpeg", 1.0);
      var pdf = new jsPDF();

      pdf.addImage(imgData, 'JPEG', 0, 0);
      pdf.save("download.pdf");
    }, false);
    </script> */
}
socket_info.onmessage = function(e) {
    console.log(e.data);
}


};

run();