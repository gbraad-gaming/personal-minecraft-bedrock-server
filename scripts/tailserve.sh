#!/bin/sh

tailscale serve --bg --tcp 19132 tcp://localhost:19132
tailscale serve --bg --tcp 19133 tcp://localhost:19133
tailscale serve --bg --tcp 19144 tcp://localhost:19144
