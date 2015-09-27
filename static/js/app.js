$(function(){
  $('#search').hide();

  $('#button').click(function() {
    $.post('image/search', function(data, status) {
      console.log(data);
    });
  });
});
