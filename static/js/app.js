$(function(){
  var link = '';
  $('#search').hide();

  $('#button').click(function() {
    $.post('post_url', function(link, status){
      console.log(link);

      $.get(link, function(data){
        tags = data['results'][0]['result']['tag']['classes'];
        console.log(tags);

        $.ajax('post_tags', {
          data : JSON.stringify(tags),
          contentType : 'application/json',
          type : 'POST',
          success: function(data) {
            console.log(data);
          }
        })
      })
    });
  });

});
