% import json


<p>Games:</p>
<table border="1">
% games = json.loads(json_games)
  %for game in games:
    % game = str(game).replace("[","")
    % game = str(game).replace("]","")
    % game = str(game).replace("'","")
    <td>{{game}}</td>
  %end
%end
</table>
