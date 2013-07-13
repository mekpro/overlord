<!DOCTYPE html>
%def leftblock():
<ul class="nav nav-list">
  <li class="nav-header">Hostlist</li>
  <li class="active"><a href="/">Overview</a></li>
  %for h in hostlist:
   <li><a href="/host?hostname={{h}}">{{h}}</a></li>
  %end
</ul>
%end

%def rightblock():
<script language="javascript" type="text/javascript" src="/assets/Jit/jit.js"></script>
<link href="/assets/Jit/Examples/css/ForceDirected.css" rel="stylesheet"/>
<script language="javascript" type="text/javascript" src="/assets/edited/force_directed.js"></script>
<script language=javascript>
  var json = {{!graph}}
//  init();
</script>

  <div class="hero-unit">
    <div id="infovis"></div>
    <div id="log"></div>
  </div>
  %i=0
  %for h in hostlist:
    %if i%3 == 0:
      <div class="row-fluid">
    %end
      <div class="span4">
        <h2>{{h}}</h2>
        <p>{{h}} information</p>
        <a class="btn" href="/host?hostname={{h}}">View details &raquo;</a>
      </div><!--/span-->
    %if i%3 == 2:
      </div>
    %end
    %i = i+1
  %end
%end

%rebase columns leftblock=leftblock, rightblock=rightblock, title=title

