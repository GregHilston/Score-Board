<!DOCTYPE html>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
	</head>

	<body>
	    <div class="container">
			<h3>{{title}}</h3>

			<div class="table-responsive">
				<table class="table border="1">
			  		% # get our JSON objects out of the list
			  		% for game, winner_dict in values.items():
			  			% for winner, loser_dict in winner_dict.items():
			  				% for loser, win in loser_dict.items():
			  					<td>{{game}} {{winner}} {{loser}} {{win}}</td>
						%end
					%end
				</table>
			</div>
		</div>

	    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	</body>
</html>