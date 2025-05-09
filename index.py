 async def fetch_logs(self) -> List[tuple]:
        """
        Fetch logs from Github using authenticated credentials.

        This method implements the actual log fetching logic and returns the
        fetched logs.

        Raises:
            exceptions.LogsFetchError: If an error occurs while fetching logs.
        """
        try:
            logs = []
            client_id = self.credentials.get('config', {}).get('client_id', '')
            account_id = {'account_id': client_id}
            access_token = self.credentials.get("config").get("access_token")
            org_name = await self.get_org_name()
            logger.info(f"Starting log fetch process for {org_name}")

            audit_logs_helper = AuditLogs(access_token=access_token, org_name=org_name)
            audit_logs = await audit_logs_helper.get_logs(self.previous_scan)
            if audit_logs:
                logs.extend(audit_logs)
            else:
                logger.info(f"No logs found for org name: {org_name}")
            return [("logs", logs, account_id)]

        except Exception as e:
            raise exceptions.LogsPullError(f"Failed to fetch logs: {str(e)}")
