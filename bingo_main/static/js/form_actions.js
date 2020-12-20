$(document).ready(function(){
  $('*[data-confirm="true"]').on('click', function() {
        return confirm($(this).data('confirm-message'));
  });
});
