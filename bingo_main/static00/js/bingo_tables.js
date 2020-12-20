$(function() {
    $.fn.shuffleTableRows = function() {
       $.each(this.get(), function(index, el) {
         var $el = $(el);
         var $find = $el.children();
          boardSize = Math.sqrt($find.length);
   
         var rows = [];
         for(var i = 0; i < $find.length; i += boardSize) {
           rows.push($find.slice(i, i+boardSize));
             }
   
         rows.sort(function() {
           return 0.5 - Math.random();
         });
   
         $el.empty();
         $el.append(rows.flat())
       });
     }
   
     setInterval(() => {
       $('.shuffleBingoTable').shuffleTableRows();
     }, 1000)
   });
   