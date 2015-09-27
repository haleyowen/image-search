$(function(){
  var searchTags = {};
  var currentWord = "";

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

        for (var tag in tags) {
          if (searchTags[tags[tag]])
            searchTags[tags[tag]] += 1;
          else
            searchTags[tags[tag]] = 1;
        }

        console.log(searchTags);

        $.ajax('post_tags', {
          type: 'POST',
          contentType: 'application/json',
          data: JSON.stringify(tags),
          success: function(data){
            data = $.parseJSON(data);
            console.log(data);

            if (data.msg.indexOf('done') < 0)
              $('#button').click();

            $('.loader-inner').hide();
          }
        });
      });
    });
  });

  function makeBubbles(){
    $.get('top_terms', function(data){
      data = $.parseJSON(data);
      for (var v in data) {
        $('#tags').append(makeButton(data[v]));
      }
    })
  }

  makeBubbles();

  function makeButton(source){
    var str = '<button type="button" class="btn btn-default" aria-label="Left Align">'  +
        '<span>'+ source +'</span>' +
        '</button>';
    return str;
  } 

  function makeTemplate(source){
    var str = '<div class="item">' +
      '<img class="thumbnail" src="' + source + '" >' +
      '</div>';
    return str;
  } 

  function addSearchTags(e){
    e.preventDefault();

    var currentWord = $('#search-box').val();
    $('#search-box').val('');
    $('#results').empty();

    $('#current').text(currentWord);

    console.log(searchTags);

    $.ajax('search', {
      data : JSON.stringify([currentWord]),
      contentType : 'application/json',
      type : 'POST',
      success: function(data) {
        data = $.parseJSON(data);

        for (var url in data) {
          $('#results').append(makeTemplate(data[url]));
        }
      }
    });
  }

  $("#search-button").click(addSearchTags);
});
