%def leftblock():
<ul class="nav nav-list">
  <li class="nav-header">Sidebar</li>
  <li class="active"><a href="/">Overview</a></li>
  %for h in hostlist:
    <li><a href="/host?hostname={{h}}">{{h}}</a></li>
  %end
</ul>
%end

%def rightblock():
<div class="hero-unit">
  <h1>{{hostname}}</h1>
  <p>Hostinfo
    <a href="/host?hostname={{hostname}}" class="btn btn-primary btn-large">&laquo Refresh &raquo;</a>
  </p>
</div>

<div>
  <h2>Ping Table</h2>
  <table class='table'>
  <tr>
    <th>Destination</th>
    <th>Last Update</th>
    <th>min</th>
    <th>max</th>
    <th>avg</th>
  </tr>
  %for row in ping_table:
  <tr>
    <td>{{row["dest"]}}</td>
    <td>{{row["dt"].strftime("%H:%M:%S")}}</td>
    <td>{{row["min"]}}</td>
    <td>{{row["max"]}}</td>
    <td>{{row["avg"]}}</td>
  </tr>
  %end
  </table>
</div>

<div>
  <h2>Iperf Table</h2>
  <table class='table'>
  <tr>
    <th>Destination</th>
    <th>Last Update</th>
    <th>Bandwidth (MB/s)</th>
  </tr>
  %for row in iperf_table: 
  <tr>
    <td>{{row["dest"]}}</td>
    <td>{{row["dt"].strftime("%H:%M:%S")}}</td>
    <td>{{round(row["bandwidth"]/1048576.0, 3)}}</td>
  </tr>
  %end
  </table>
</div>
          
<div>
  <h2>Network Utilization</h2>
</div>
%end 

%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
