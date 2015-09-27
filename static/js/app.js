$(function(){
  var link = '';
  var searchTags = [];

  $('#search').hide();

  $('#button').click(function() {
    $('.loader-inner').show();
    
    $.post('post_url', function(link, status){
      console.log(link);

      if(link.indexOf('http') < 0) {
        $('.loader-inner').hide();
        return;
      }

      $.get(link, function(data){
        tags = data['results'][0]['result']['tag']['classes'];
        console.log(tags);

        $.ajax('post_tags', {
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(tags),
          success: function(data){
            console.log(data);
            $('.loader-inner').hide();
          }
        });
      });
    });
  });

  function makeTemplate(source){
    return '<img class="pic" src="' + source + '" >';
  } 

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
        data = $.parseJSON(data);
        $('#results').empty();
        for (var url in data) {
          console.log(url);
          $('#results').append(makeTemplate(data[url]));
        }
      }
    });
  }

  $("#search-button").click(addSearchTags);
});
