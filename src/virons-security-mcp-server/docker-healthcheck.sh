#!/bin/sh
# Copyright Virons Fintech. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

SERVER="virons-security-mcp-server"

# Check if the server process is running
if pgrep -f "virons.security_mcp_server" > /dev/null; then
  echo "$SERVER is running"
  exit 0
fi

# Unhealthy
echo "$SERVER is not running"
exit 1
