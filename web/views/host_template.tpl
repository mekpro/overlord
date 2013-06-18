<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Network Status: {{hostname}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Le styles -->
    <link href="../assets/css/bootstrap.css" rel="stylesheet">

    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      .sidebar-nav {
        padding: 9px 0;
      }

      @media (max-width: 980px) {
        /* Enable use of floated navbar text */
        .navbar-text.pull-right {
          float: none;
          padding-left: 5px;
          padding-right: 5px;
        }
      }
    </style>
    <link href="../assets/css/bootstrap-responsive.css" rel="stylesheet">
    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="../assets/js/html5shiv.js"></script>
    <![endif]-->

  </head>
  <body>


    <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="brand" href="#">Network Status</a>
          <div class="nav-collapse collapse">
           <ul class="nav">
              <li class="active"><a href="#">Home</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span3">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Sidebar</li>
              <li class="active"><a href="/">Overview</a></li>
              %for h in hostlist:
               <li><a href="/host?hostname={{h}}">{{h}}</a></li>
              %end
            </ul>
          </div><!--/.well -->
        </div><!--/span-->
        <div class="span9">
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

              </tr>
            </table>
          </div>
          <div>
            <h2>Network Utilization</h2>

          </div>
          </div><!--/row-->
        </div><!--/span-->
      </div><!--/row-->

      <hr>

      <footer>
        <p>Network Monitoring: Web UI (mekpro@gmail.com)</p>
      </footer>

    </div><!--/.fluid-container-->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../assets/js/jquery.js"></script>
    <script src="../assets/js/bootstrap-transition.js"></script>
    <script src="../assets/js/bootstrap-alert.js"></script>
    <script src="../assets/js/bootstrap-modal.js"></script>
    <script src="../assets/js/bootstrap-dropdown.js"></script>
    <script src="../assets/js/bootstrap-scrollspy.js"></script>
    <script src="../assets/js/bootstrap-tab.js"></script>
    <script src="../assets/js/bootstrap-tooltip.js"></script>
    <script src="../assets/js/bootstrap-popover.js"></script>
    <script src="../assets/js/bootstrap-button.js"></script>
    <script src="../assets/js/bootstrap-collapse.js"></script>
    <script src="../assets/js/bootstrap-carousel.js"></script>
    <script src="../assets/js/bootstrap-typeahead.js"></script>

  </body>
</html>
