<!DOCTYPE html>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
	</head>

	<body>
	    <div class="container">
			<h3>{{title}}</h3>

			<table border="1">
			  %for val in values:
			    % val = val[0] # get our JSON object out of the list
			    <td>{{val}}</td>
			  %end
			%end
			</table>
		</div>

	    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	</body>
</html>