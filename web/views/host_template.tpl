%def leftblock():
<ul class="nav nav-list">
  <li class="nav-header">Sidebar</li>
  <li class="active"><a href="/">Overview</a></li>
  %for h in hostlist:
    <li><a href="/host/{{h}}">{{h}}</a></li>
  %end
</ul>
%end

%def rightblock():
<div class="hero-unit">
  <h1>{{hostname}}</h1>
  <p>Bandwidth Graph
    <a href="/host/{{hostname}}" class="btn btn-primary btn-large">&laquo Refresh &raquo;</a>
  </p>
  <div id=line_graph>
    <svg style='height:500px'> </svg>
  </div>

<script type="text/javascript">
d3.json('/api/query/host/{{hostname}}/iperf/bandwidth?dt_start={{dt_start}}&dt_end={{dt_end}}', function (data) {
  nv.addGraph(function() {
    var testdata = data,
        chart = nv.models.lineChart()
          .margin({top: 30, right: 20, bottom: 30, left: 60})
          .x(function(d,i) { return i })
          .color(d3.scale.category10().range());

    chart.xAxis.tickFormat(function(d) {
      keys = Object.keys(data['result']);
      var dx = data['result'][keys[0]][d][0] ;
      return d3.time.format('%X')(new Date(dx*1000));
    });

    chart.yAxis
        .tickFormat(function(d) { return d3.format(',f')(d) + 'MB/s'});

//    chart.bars.forceY([0]);
//    chart.lines.forceY([0]);
      bwdatum = []
      for (var k in data['result']) {
        d = {
          "key" : k,
          "values" : data['result'][k]
          };
        bwdatum.push(d);
      }
      d3.select('#line_graph svg')
          .datum(bwdatum.map(function(series) {
            series.values = series.values.map(function(d) { return {x: d[0], y: d[1] } });
            return series;}))
      .transition().duration(500).call(chart);

      nv.utils.windowResize(chart.update);

      return chart;
    });
});

function exampleData() {
  return [ 
    { 
      "key" : "Quantity" , 
      "bar": true,
      "values" : [ [ 1136005200000 , 1271000.0] , [ 1138683600000 , 1271000.0] , [ 1141102800000 , 1271000.0] , [ 1143781200000 , 0] , [ 1146369600000 , 0] , [ 1149048000000 , 0] , [ 1151640000000 , 0] , [ 1154318400000 , 0] , [ 1156996800000 , 0] , [ 1159588800000 , 3899486.0] , [ 1162270800000 , 3899486.0] , [ 1164862800000 , 3899486.0] , [ 1167541200000 , 3564700.0] , [ 1170219600000 , 3564700.0] , [ 1172638800000 , 3564700.0] , [ 1175313600000 , 2648493.0] , [ 1177905600000 , 2648493.0] , [ 1180584000000 , 2648493.0] , [ 1183176000000 , 2522993.0] , [ 1185854400000 , 2522993.0] , [ 1188532800000 , 2522993.0] , [ 1191124800000 , 2906501.0] , [ 1193803200000 , 2906501.0] , [ 1196398800000 , 2906501.0] , [ 1199077200000 , 2206761.0] , [ 1201755600000 , 2206761.0] , [ 1204261200000 , 2206761.0] , [ 1206936000000 , 2287726.0] , [ 1209528000000 , 2287726.0] , [ 1212206400000 , 2287726.0] , [ 1214798400000 , 2732646.0] , [ 1217476800000 , 2732646.0] , [ 1220155200000 , 2732646.0] , [ 1222747200000 , 2599196.0] , [ 1225425600000 , 2599196.0] , [ 1228021200000 , 2599196.0] , [ 1230699600000 , 1924387.0] , [ 1233378000000 , 1924387.0] , [ 1235797200000 , 1924387.0] , [ 1238472000000 , 1756311.0] , [ 1241064000000 , 1756311.0] , [ 1243742400000 , 1756311.0] , [ 1246334400000 , 1743470.0] , [ 1249012800000 , 1743470.0] , [ 1251691200000 , 1743470.0] , [ 1254283200000 , 1519010.0] , [ 1256961600000 , 1519010.0] , [ 1259557200000 , 1519010.0] , [ 1262235600000 , 1591444.0] , [ 1264914000000 , 1591444.0] , [ 1267333200000 , 1591444.0] , [ 1270008000000 , 1543784.0] , [ 1272600000000 , 1543784.0] , [ 1275278400000 , 1543784.0] , [ 1277870400000 , 1309915.0] , [ 1280548800000 , 1309915.0] , [ 1283227200000 , 1309915.0] , [ 1285819200000 , 1331875.0] , [ 1288497600000 , 1331875.0] , [ 1291093200000 , 1331875.0] , [ 1293771600000 , 1331875.0] , [ 1296450000000 , 1154695.0] , [ 1298869200000 , 1154695.0] , [ 1301544000000 , 1194025.0] , [ 1304136000000 , 1194025.0] , [ 1306814400000 , 1194025.0] , [ 1309406400000 , 1194025.0] , [ 1312084800000 , 1194025.0] , [ 1314763200000 , 1244525.0] , [ 1317355200000 , 475000.0] , [ 1320033600000 , 475000.0] , [ 1322629200000 , 475000.0] , [ 1325307600000 , 690033.0] , [ 1327986000000 , 690033.0] , [ 1330491600000 , 690033.0] , [ 1333166400000 , 514733.0] , [ 1335758400000 , 514733.0]]
    } , 

    { 
      "key" : "Price" , 
      "values" : [ [ 1136005200000 , 71.89] , [ 1138683600000 , 75.51] , [ 1141102800000 , 68.49] , [ 1143781200000 , 62.72] , [ 1146369600000 , 70.39] , [ 1149048000000 , 59.77] , [ 1151640000000 , 57.27] , [ 1154318400000 , 67.96] , [ 1156996800000 , 67.85] , [ 1159588800000 , 76.98] , [ 1162270800000 , 81.08] , [ 1164862800000 , 91.66] , [ 1167541200000 , 84.84] , [ 1170219600000 , 85.73] , [ 1172638800000 , 84.61] , [ 1175313600000 , 92.91] , [ 1177905600000 , 99.8] , [ 1180584000000 , 121.191] , [ 1183176000000 , 122.04] , [ 1185854400000 , 131.76] , [ 1188532800000 , 138.48] , [ 1191124800000 , 153.47] , [ 1193803200000 , 189.95] , [ 1196398800000 , 182.22] , [ 1199077200000 , 198.08] , [ 1201755600000 , 135.36] , [ 1204261200000 , 125.02] , [ 1206936000000 , 143.5] , [ 1209528000000 , 173.95] , [ 1212206400000 , 188.75] , [ 1214798400000 , 167.44] , [ 1217476800000 , 158.95] , [ 1220155200000 , 169.53] , [ 1222747200000 , 113.66] , [ 1225425600000 , 107.59] , [ 1228021200000 , 92.67] , [ 1230699600000 , 85.35] , [ 1233378000000 , 90.13] , [ 1235797200000 , 89.31] , [ 1238472000000 , 105.12] , [ 1241064000000 , 125.83] , [ 1243742400000 , 135.81] , [ 1246334400000 , 142.43] , [ 1249012800000 , 163.39] , [ 1251691200000 , 168.21] , [ 1254283200000 , 185.35] , [ 1256961600000 , 188.5] , [ 1259557200000 , 199.91] , [ 1262235600000 , 210.732] , [ 1264914000000 , 192.063] , [ 1267333200000 , 204.62] , [ 1270008000000 , 235.0] , [ 1272600000000 , 261.09] , [ 1275278400000 , 256.88] , [ 1277870400000 , 251.53] , [ 1280548800000 , 257.25] , [ 1283227200000 , 243.1] , [ 1285819200000 , 283.75] , [ 1288497600000 , 300.98] , [ 1291093200000 , 311.15] , [ 1293771600000 , 322.56] , [ 1296450000000 , 339.32] , [ 1298869200000 , 353.21] , [ 1301544000000 , 348.5075] , [ 1304136000000 , 350.13] , [ 1306814400000 , 347.83] , [ 1309406400000 , 335.67] , [ 1312084800000 , 390.48] , [ 1314763200000 , 384.83] , [ 1317355200000 , 381.32] , [ 1320033600000 , 404.78] , [ 1322629200000 , 382.2] , [ 1325307600000 , 405.0] , [ 1327986000000 , 456.48] , [ 1330491600000 , 542.44] , [ 1333166400000 , 599.55] , [ 1335758400000 , 583.98]]
    }
  ].map(function(series) {
    series.values = series.values.map(function(d) { return {x: d[0], y: d[1] } });
    return series;
  }); 
}
</script>

</div>
<div>
   <div id='datetimebox'>
     <h3>Time Range</h3>
     <form method="POST">
       <a>begin</a>
       <div id="start_datetimepicker" class="input-append date">
          <input type="text" name="dt_start"></input>
          <span class="add-on">
            <i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>
          </span>
       </div>

       <a>end:</a>
       <div id="end_datetimepicker" class="input-append date">
          <input type="text" name="dt_end"></input>
          <span class="add-on">
            <i data-time-icon="icon-time" data-date-icon="icon-calendar"></i>
          </span>
       </div>
       <input type="submit" value="refresh">
     </form>
  </div>
  <h3>Latency (ms)</h3>
  <table class='table'>
  <tr>
    <th>Destination</th>
    <th>Last Update</th>
    <th>Average</th>
    <th>Count</th>
    <th>Min</th>
    <th>Max</th>
    <th>S.D.</th>
    <th>Var</th>
  </tr>
  %for k,v in ping_table.items(): 
  <tr>
    <td>{{k}}</td>
    <td>{{v["last_dt"].strftime("%H:%M:%S")}}</td>
    <td>{{round(v["avg"],1)}}</td>
    <td>{{int(v["count"])}}</td>
    <td>{{v["min"]}}</td>
    <td>{{v["max"]}}</td>
    <td>{{round(v["stddev"],2)}}</td>
    <td>{{round(v["variance"],2)}}</td>
  </tr>
  %end
  </table>
</div>

<div>
  <h3>Bandwidth(MB/s)</h3>
  <table class='table'>
  <tr>
    <th>Destination</th>
    <th>Last Update</th>
    <th>Average</th>
    <th>Count</th>
    <th>Min</th>
    <th>Max</th>
    <th>S.D.</th>
    <th>Var</th>
  </tr>
  %for k,v in iperf_table.items(): 
  <tr>
    <td>{{k}}</td>
    <td>{{v["last_dt"].strftime("%H:%M:%S")}}</td>
    <td>{{round(v["avg"],1)}}</td>
    <td>{{int(v["count"])}}</td>
    <td>{{v["min"]}}</td>
    <td>{{v["max"]}}</td>
    <td>{{round(v["stddev"],2)}}</td>
    <td>{{round(v["variance"],2)}}</td>
  </tr>
  %end
  </table>
</div>
          
<div>
  <h2>Network Utilization</h2>
</div>

<script type="text/javascript">
  $('#start_datetimepicker').datetimepicker({format: 'dd/MM/yyyy hh:mm:ss',});
  $('#end_datetimepicker').datetimepicker({format: 'dd/MM/yyyy hh:mm:ss',});
</script>
%end 

%rebase columns leftblock=leftblock, rightblock=rightblock, title=title
