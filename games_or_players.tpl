<div class="container">
	<h2>{{title}}</h2>

	<div class="table-responsive">
		<table class="table border="1">
		  %for val in values:
		    % val = val[0] # get our JSON object out of the list
		    <td>{{val}}</td>
		  %end
		%end
		</table>
	</div>
</div>