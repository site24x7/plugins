
Plugin for Zombies Process Monitoring
======================================

This plugin is for calculating the number of "zombie" processes created in the server.
  

PreRequisites
=============

Download zombies plugin from https://github.com/site24x7/plugins/blob/master/zombies/zombies.py.
Place the plugin folder 'zombies/zombies.py' under agent plugins directory (/opt/site24x7/monagent/plugins/).
Our plugin uses 'top' command to get the number of zombies process count.


Metrics
========
Reports back the number of zombies process present in the server.
