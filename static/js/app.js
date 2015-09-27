$(function(){
  var link = '';
  var searchTags = [];

  $('#search').hide();

  $('#button').click(function() {

    $('.loader-inner').show();
    
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
            $('.loader-inner').hide();
          }
        });

      });

    });

  });

  function addSearchTags(e){
    e.preventDefault();

    searchTags.push($('#search-box').val());
    $('#search-box').val('');

    console.log(searchTags);

    $.ajax('search', {
      data : JSON.stringify(searchTags),
      contentType : 'application/json',
      type : 'POST',
      success: function(data) {
        console.log(data);
      }
    });
  }

  $("#search-button").click(addSearchTags);
});
