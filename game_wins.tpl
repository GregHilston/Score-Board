% for game, winner_dict in values.items():
	<div class="container reloadable-{{game}}">
		<h2>{{game}}</h2>

		<div class="table-responsive">
			<table class="table border="1">
				<thead>
					<tr>
						<th>Winner</th>
						<th>Loser</th>
						<th>Wins</th>
					</tr>
				</thead>

				<tbody>
		  			% for winner, loser_dict in winner_dict.items():
		  				% for loser, win in loser_dict.items():
		  					<tr>
		  						<td>{{winner}}</td>
		  						<td>{{loser}}</td>
		  						% print(f"win {win}")
		  						<td>{{win}}</td>
		  					</tr>
		  				% end
					% end
				</tbody>
			</table>
		</div>
	</div>
% end