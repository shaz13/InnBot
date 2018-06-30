$(document).ready(function(){

setTimeout(function () {
$('#query').inputfit();
$('#query').fadeTo( "1000", 1.0 )
}, 2000); // Execute something() 1 second later.



if ('addEventListener' in window) {
			window.addEventListener('load', function() { document.body.className = document.body.className.replace(/\bis-loading\b/, ''); });
			document.body.className += (navigator.userAgent.match(/(MSIE|rv:11\.0)/) ? ' is-ie' : '');
		}

		var eva_url = "http://127.0.0.1:5000/api/AskInn";
		var result;

			$("#btn").click(function() {

				console.log($("#query").val())
		    var result = $.ajax({
		        type: "POST",
		        url: eva_url,
		        data:JSON.stringify({
					"query": $("#query").val(),
				}),  
		        success: function(data) {
					console.log(data)
					$('#output').html('');
      var p = data

      for (var key in p) {
        if (p.hasOwnProperty(key)) {
          $("#output").append("<tr class='output_table'><td class='output_table'>" + key + "</td><td>" + p[key] + "</td><tr/>");
        }
      }



		        }
		    });
		});
 });
