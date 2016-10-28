$(document).ready(function() {
    $('input#date').change(function() {
        var date = $(this).val();
        if(date)  update_date();
        else  $('div#results').html('');
    })
    $('div#results').on('change', 'select#rest', function() {
        var choice = $(this).val();
        if(choice) {
            $.ajax({
                method : 'post',
                url : $('form#choice').attr('action'),  // '/bites/show/restaurant'
                data : $('form#choice').serialize(),
                success : function(resp){
                              $('div#user').html(resp);
                          }
            })
        }
        else  update_date();
    })
    $('div#results').on('click', 'button#join', function() {
        var choice_id =  $(this).attr("title");
        var url = "/bites/join/"+choice_id;
        console.log("URL:", url);
        $.ajax({
            method : 'get',
            url : url,
            success : function(resp){
                        console.log("Response:", resp);
                      }
        })
        update_date();
    })
    $('div#results').on('click', 'button#unjoin', function() {
        var choice_id =  $(this).attr("title");
        var url = "/bites/unjoin/"+choice_id;
        console.log("URL:", url);
        $.ajax({
            method : 'get',
            url : url,
            success : function(resp){
                        console.log("Response:", resp);
                      }
        })
        update_date();
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
})
