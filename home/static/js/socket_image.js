function getParagraph(block) {
    //this function gonna return a bunch of words in a block
    var res = [];
    var paras = block['paragraphs'];
    for (i in paras) {
        var para = paras[i];
        res = res.concat(getWord(para));
    }
    return res;
}

function getWord(para) {
    var res = [];
    var words = para['words'];
    for (i in words) {
        var word = words[i];
        var coordinate = word['boundingBox'];
        res.push({ 'text': getSym(word), 'boundingBox': coordinate });
    }
    // console.log(res);
    return res;
}

function getMainPath(ans) {
    var res = [];
    var start = 0;
    var end = 0;
    for (path in ans) {
        for (text in ans[path]) {
            if (ans[path][text].includes('Mặt hàng')) {
                // console.log('reached here!');
                start = Number(path) + 1;
                break;
            }
        }
        for (text in ans[path]) {
            if (ans[path][text].includes('TỔNG')) {
                // console.log('reached here!');
                end = Number(path);
                break;
            }
        }
    }
    console.log(start, end);
    for (i = start; i < end; i++) {
        res.push(ans[i]);
    }
    console.log(ans);
    return res;
}

function merge(strarr) {
    var res = '';
    for (k = 0; k < strarr.length; k++) {
        res += strarr[k] + "";
    }
    return res;
}

function split_value_line(product_name, line) {
    var product_code = line[0];
    var product_value = line[1];
    var product_count = line[2];
    var sum = line[3];
    console.log('type of sum', typeof sum);
    console.log('type of product_value', typeof product_value);
    return {
        'product_name': merge(product_name),
        'product_code': product_code,
        'product_value': product_value.replace(/' '/g, ''),
        'product_count': product_count,
        'sum': sum,
        'km': 0
    };
}

function getTable(res) {
    //return json object 
    var ans = [];
    for (i = 0; i < res.length - 1; i++) {
        for (j = 0; j < res[i].length; j++) {
            var str = res[i][j];
            if (str.charCodeAt(0) < 48 || str.charCodeAt(0) > 57) {
                // console.log(res[i+1][0], Number(res[i+1][0]));
                if (Number.isNaN(Number(res[i + 1][0])) == true) {
                    break;
                }
                if (res[i + 1].length < 3) {
                    break;
                }
                console.log('line', res[i + 1][0], res[i + 1][0] == NaN)
                    // console.log('reached', res[i][j])
                var result = split_value_line(res[i], res[i + 1]);
                if (i + 2 < res.length) {
                    if (res[i + 2][res[i + 2].length - 1].charAt(0) == '-') {
                        result['km'] = res[i + 2][res[i + 2].length - 1];
                        i += 1;
                    };
                }
                ans.push(result);
                i += 1;
                break;
            }
        }
    }
    return ans;
    // console.log(ans);
}

function getSym(word) {
    var res = '';
    var symbols = word['symbols'];
    for (i in symbols) {
        res += symbols[i]['text'];
    }
    return res;
}

function checkNumber(text) {
    if (Number(text) != NaN) return true;
}
//take the boundingbox object
function merge_box(boxs) {
    // var minx = 10000, maxx = -1, miny = 10000, maxy = -1;
    var text = '';
    // console.log(boxs);
    for (box in boxs) {
        text += boxs[box].text;
        if (box != boxs.length - 1)
            text += ' ';
    }

    return text;
}
// Sửa hàm này !
function merge_text(w) {
    console.log(w);
    var res = [];
    var words = w['words'];
    var index = 0;

    words.sort(function(a, b) {
        var y1 = b['boundingBox']['vertices'][3]['y'];
        var y2 = a['boundingBox']['vertices'][3]['y'];
        var x1 = b['boundingBox']['vertices'][3]['x'];
        var x2 = a['boundingBox']['vertices'][3]['x'];
        if (y1 - y2 > 10) return -1;
        else if (Math.abs(y1 - y2) <= 10 && x2 < x1) return -1;
        else if (Math.abs(y1 - y2) <= 10 && x2 > x1) return 0;
        else return 1;
    });
    //Remember always keep the coordinate, that make the world
    var count = 0;
    while (index <= words.length - 1) {
        res.push([]);
        var temp = words[index];
        res[count].push(temp);
        if (index < words.length - 2) {
            while (Math.abs(words[index]['boundingBox']['vertices'][3]['y'] - words[index + 1]['boundingBox']['vertices'][3]['y']) < 10) {
                temp = words[index + 1];
                res[count].push(temp);
                index += 1;
                if (index >= words.length - 1) {
                    break;
                }
            }
        }
        index += 1;
        count++;
    }
    console.log(res);
    //Merging the fucking text
    //is under there
    //stupid patheic

    var ans = [];
    var i = 0;
    var res2 = [];

    //merge the texts that are splited by google API first, then use 
    //another function to merge their coordinates
    for (i = 0; i < count; i++) {
        res2.push([]);
        for (j = 0; j < res[i].length; j++) {
            var list_to_merge = [];
            list_to_merge.push(res[i][j]);
            while (j < res[i].length - 1) {
                if (Math.abs(res[i][j].boundingBox.vertices[2].x - res[i][j + 1].boundingBox.vertices[3].x) <= 18) {
                    list_to_merge.push(res[i][j + 1]);
                    j++;
                } else {
                    break;
                }
            }
            res2[i].push(merge_box(list_to_merge));
        }
    }
    console.log(res2);
    return res2;
}



function run() {
    endpoint = 'ws://' + window.location.host + '/message/';
    console.log(window.location.host)
    var socket = new ReconnectingWebSocket(endpoint);

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

    socket.onmessage = function(e) {
        console.log(e);
        var responseData = JSON.parse(e.data);
        var file_name = 'data:image/png;base64,' + responseData.base64;
        $('#images').append($('<div class="clickable_img" onclick="show_img_details(\'' +
            file_name + ' \')"> <img width = \"100\" class="img-fluid img-thumbnail" alt=\"Avatar\"src=\"data:image/png; base64, ' +
            responseData.base64 + '\
                    "></div>'));
        var text_data = JSON.parse(responseData.Question);
        console.log(text_data)
        for (ans in text_data) {
            $('#result').append($('<div class="form-group"><h3><div class="list-group-item "><label for="first_name"><h4>' +
                text_data[ans]['text'] + '</h4></label><input style="background-color:rgb(63, 54, 78) " type="text" class="form-control" name="input" id="first_name"></div></h3></div>'));
            console.log(text_data[ans]['text']);
        }
        $('#result').append($('<div class="form-group "><div class="form-group "><div class="col-xs-12 "><button class="btn btn-lg btn-success " ><i class="glyphicon glyphicon-ok-sign "></i> Save</button></div></div></div>'));



    };


};

$('#result').submit(function() {
    // get all the inputs into an array.
    var $inputs = $('#result :input');

    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    var values = {};
    console.log(values)
    $inputs.each(function() {
        values[this.name] = $(this).val();
    });
    console.log(values);
});
run();