$(document).ready(function() {
    $('input#date').change(function() {
        var date = $(this).val();
        if(date)  update_date();
        else $('div#results').html("<p class='hint'>Please select a date!</p>");
    })
    $('div#results').on('change', 'select#rest', function() {
        var choice = $(this).val();
        var date = $('input#date').val();
        if(choice) {
            var serialized = $('form#choice').serialize()+'&date='+date;
            $.ajax({
                method : 'post',
                url : $('form#choice').attr('action'),  // '/bites/show/restaurant'
                data : serialized,
                success : function(resp){
                              $('div#restaurant').html(resp);
                          }
            })
        }
        else  update_date();
    })
    $('div#results').on('click', 'button', function() {
        var choice_id =  $(this).attr("title");
        var action = $(this).attr("id");
        if(action == 'join') var url = "/bites/join/"+choice_id;
        else  var url = "/bites/unjoin/"+choice_id;
        console.log("URL:", url);
        $.ajax({
            method : 'get',
            url : url,
            success : function(resp){
                        console.log("Response:", resp);
                        update_date();
                      }
        })

    })
    function update_date() {
        $.ajax({
            method : 'post',
            url : $('form#date').attr('action'),  // '/bites/show/choice'
            data : $('form#date').serialize(),
            success : function(resp){
                $('div#results').html(resp);
            }
        })
    }

    $('span.direct').click(function() {
        var rest_id = $(this).attr('id');
        var url = '/bites/show/direction/'+rest_id
        $.ajax({
            url : url,
            method : 'get',
            success : function(res) {
                // console.log("RES:",res);
                $('div#directions').html(res)
            }
        })
    })
    // window.onload = function() {
    //     var today = $('body').attr('id');
    //     var serialized = $('form#date').serialize()+today;
    //     $.ajax({
    //         method : 'post',
    //         url : '/bites/show/choice',
    //         data : serialized,
    //         success : function(resp){
    //             $('div#results').html(resp);
    //         }
    //     })
    // }
})
