<p>Record a Win</p>

<form action="/add_record" method="post">
  Game
  <select name="game">
      %for game in games:
      % game = game[0] # get our JSON object out of the list
      <option value="{{game}}">{{game}}</option>
      %end
  </select>

  Winner
  <select name="winner">
      %for player in players:
      % player = player[0] # get our JSON object out of the list
      <option value="{{player}}">{{player}}</option>
      %end
  </select>

  Loser
  <select name="loser">
      %for player in players:
      % player = player[0] # get our JSON object out of the list
      <option value="{{player}}">{{player}}</option>
      %end
  </select>

    <input type="submit" value="Submit">
</form>
