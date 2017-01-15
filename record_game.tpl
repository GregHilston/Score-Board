<p>Record a Win</p>

<form action="/add_record" method="post">
  <select name="gamelist">
      %for game in games:
      <option value="{{game}}">{{game}}</option>
      %end
  </select>
</form>
