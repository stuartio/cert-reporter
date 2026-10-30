from typing import Optional
from .base import Akamai


# CPS v2 uses vendor media types for both Accept and Content-Type. Versions are the latest
# documented for each operation in the CPS v2 OpenAPI spec.
ACTIVE_CERTIFICATES = "application/vnd.akamai.cps.active-certificates.v2+json"
CERTIFICATE_HISTORY = "application/vnd.akamai.cps.certificate-history.v2+json"
CHANGE = "application/vnd.akamai.cps.change.v2+json"
CHANGE_HISTORY = "application/vnd.akamai.cps.change-history.v5+json"
CHANGE_ID = "application/vnd.akamai.cps.change-id.v1+json"
DEPLOYMENT = "application/vnd.akamai.cps.deployment.v8+json"
DEPLOYMENT_SCHEDULE = "application/vnd.akamai.cps.deployment-schedule.v1+json"
DEPLOYMENTS = "application/vnd.akamai.cps.deployments.v8+json"
DV_HISTORY = "application/vnd.akamai.cps.dv-history.v1+json"
ENROLLMENT = "application/vnd.akamai.cps.enrollment.v12+json"
ENROLLMENT_STATUS = "application/vnd.akamai.cps.enrollment-status.v1+json"
ENROLLMENTS = "application/vnd.akamai.cps.enrollments.v11+json"

# The Accept header for reading a change input depends on the input type (the last segment of
# Change.allowedInput[].info). The Content-Type for updating it depends on the update type
# (the last segment of Change.allowedInput[].update).
CHANGE_INPUT_INFO_ACCEPT = {
    "change-management-info": "application/vnd.akamai.cps.change-management-info.v6+json",
    "lets-encrypt-challenges": "application/vnd.akamai.cps.dv-challenges.v2+json",
    "post-verification-warnings": "application/vnd.akamai.cps.warnings.v1+json",
    "pre-verification-warnings": "application/vnd.akamai.cps.warnings.v1+json",
    "third-party-csr": "application/vnd.akamai.cps.csr.v2+json",
}
CHANGE_INPUT_UPDATE_CONTENT_TYPE = {
    "change-management-ack": "application/vnd.akamai.cps.acknowledgement.v1+json",
    "lets-encrypt-challenges-completed": "application/vnd.akamai.cps.acknowledgement.v1+json",
    "post-verification-warnings-ack": "application/vnd.akamai.cps.acknowledgement-with-hash.v1+json",
    "pre-verification-warnings-ack": "application/vnd.akamai.cps.acknowledgement-with-hash.v1+json",
    "third-party-cert-and-trust-chain": "application/vnd.akamai.cps.certificate-and-trust-chain.v2+json",
}


class AkamaiCPS(Akamai):
    # Certificates
    def get_active_certificates(self, contract_id: str) -> list:
        """
        List enrollments with active certificates.

        Args:
            contract_id: Contract ID to filter enrollments

        Returns:
            List of enrollments with active certificates
        """
        path = "/cps/v2/active-certificates"
        params = {"contractId": contract_id}
        result = self.get(path=path, params=params, headers={"accept": ACTIVE_CERTIFICATES})
        return result["enrollments"]

    # Enrollments
    def list_enrollments(self, contract_id: Optional[str] = None) -> list:
        """
        List certificate enrollments.

        Args:
            contract_id: Optional contract ID to filter enrollments

        Returns:
            List of enrollments
        """
        path = "/cps/v2/enrollments"
        params = {"contractId": contract_id} if contract_id is not None else None
        result = self.get(path=path, params=params, headers={"accept": ENROLLMENTS})
        return result["enrollments"]

    def create_enrollment(
        self, enrollment_data: dict, contract_id: str, allow_duplicate_cn: Optional[bool] = None
    ) -> dict:
        """
        Create a new certificate enrollment.

        Args:
            enrollment_data: Enrollment configuration
            contract_id: Contract ID for the enrollment
            allow_duplicate_cn: Allow duplicate common names

        Returns:
            Created enrollment response
        """
        path = "/cps/v2/enrollments"
        params = {"contractId": contract_id}
        if allow_duplicate_cn is not None:
            params["allow-duplicate-cn"] = "true" if allow_duplicate_cn else "false"
        headers = {"content-type": ENROLLMENT, "accept": ENROLLMENT_STATUS}
        return self.post(path=path, params=params, headers=headers, body=enrollment_data)

    def get_enrollment(self, enrollment_id: int) -> dict:
        """
        Get enrollment details.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Enrollment details
        """
        path = f"/cps/v2/enrollments/{enrollment_id}"
        return self.get(path=path, headers={"accept": ENROLLMENT})

    def update_enrollment(
        self, enrollment_id: int, enrollment_data: dict, allow_cancel_pending_changes: Optional[bool] = None
    ) -> dict:
        """
        Update an enrollment.

        Args:
            enrollment_id: The enrollment ID
            enrollment_data: Updated enrollment configuration
            allow_cancel_pending_changes: Allow canceling pending changes

        Returns:
            Update response
        """
        path = f"/cps/v2/enrollments/{enrollment_id}"
        params = (
            {"allow-cancel-pending-changes": "true" if allow_cancel_pending_changes else "false"}
            if allow_cancel_pending_changes is not None
            else None
        )
        headers = {"content-type": ENROLLMENT, "accept": ENROLLMENT_STATUS}
        return self.put(path=path, params=params, headers=headers, body=enrollment_data)

    def delete_enrollment(self, enrollment_id: int) -> dict:
        """
        Delete an enrollment.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Delete response
        """
        path = f"/cps/v2/enrollments/{enrollment_id}"
        return self.delete(path=path, headers={"accept": ENROLLMENT_STATUS})

    # Changes
    def get_change(self, enrollment_id: int, change_id: int) -> dict:
        """
        Get details of a pending change.

        Args:
            enrollment_id: The enrollment ID
            change_id: The change ID

        Returns:
            Change details
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/changes/{change_id}"
        return self.get(path=path, headers={"accept": CHANGE})

    def delete_change(self, enrollment_id: int, change_id: int) -> dict:
        """
        Cancel a pending change.

        Args:
            enrollment_id: The enrollment ID
            change_id: The change ID

        Returns:
            Cancel response
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/changes/{change_id}"
        return self.delete(path=path, headers={"accept": CHANGE_ID})

    def get_deployment_schedule(self, enrollment_id: int, change_id: int) -> dict:
        """
        Get deployment schedule for a change.

        Args:
            enrollment_id: The enrollment ID
            change_id: The change ID

        Returns:
            Deployment schedule
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/changes/{change_id}/deployment-schedule"
        return self.get(path=path, headers={"accept": DEPLOYMENT_SCHEDULE})

    def update_deployment_schedule(self, enrollment_id: int, change_id: int, schedule_data: dict) -> dict:
        """
        Update deployment schedule for a change.

        Args:
            enrollment_id: The enrollment ID
            change_id: The change ID
            schedule_data: Schedule configuration

        Returns:
            Update response
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/changes/{change_id}/deployment-schedule"
        headers = {"content-type": DEPLOYMENT_SCHEDULE, "accept": CHANGE_ID}
        return self.put(path=path, headers=headers, body=schedule_data)

    def get_change_allowed_input_param(self, enrollment_id: int, change_id: int, allowed_input_type: str) -> dict:
        """
        Get allowed input parameters for a change.

        Args:
            enrollment_id: The enrollment ID
            change_id: The change ID
            allowed_input_type: Type of allowed input

        Returns:
            Allowed input parameters
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/changes/{change_id}/input/info/{allowed_input_type}"
        if allowed_input_type not in CHANGE_INPUT_INFO_ACCEPT:
            raise ValueError(f"Unsupported allowed input type '{allowed_input_type}'")
        return self.get(path=path, headers={"accept": CHANGE_INPUT_INFO_ACCEPT[allowed_input_type]})

    def update_change_allowed_input(
        self, enrollment_id: int, change_id: int, allowed_input_type: str, input_data: dict
    ) -> dict:
        """
        Update allowed input for a change.

        Args:
            enrollment_id: The enrollment ID
            change_id: The change ID
            allowed_input_type: Type of allowed input
            input_data: Input data to update

        Returns:
            Update response
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/changes/{change_id}/input/update/{allowed_input_type}"
        if allowed_input_type not in CHANGE_INPUT_UPDATE_CONTENT_TYPE:
            raise ValueError(f"Unsupported allowed input type '{allowed_input_type}'")
        headers = {"content-type": CHANGE_INPUT_UPDATE_CONTENT_TYPE[allowed_input_type], "accept": CHANGE_ID}
        return self.post(path=path, headers=headers, body=input_data)

    # Deployments
    def list_deployments(self, enrollment_id: int) -> dict:
        """
        List deployments for an enrollment.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Deployment information
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/deployments"
        return self.get(path=path, headers={"accept": DEPLOYMENTS})

    def get_production_deployment(self, enrollment_id: int) -> dict:
        """
        Get production deployment details.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Production deployment details
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/deployments/production"
        return self.get(path=path, headers={"accept": DEPLOYMENT})

    def get_staging_deployment(self, enrollment_id: int) -> dict:
        """
        Get staging deployment details.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Staging deployment details
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/deployments/staging"
        return self.get(path=path, headers={"accept": DEPLOYMENT})

    # History
    def get_dv_history(self, enrollment_id: int) -> dict:
        """
        Get domain validation history.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            DV history
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/dv-history"
        return self.get(path=path, headers={"accept": DV_HISTORY})

    def get_certificate_history(self, enrollment_id: int) -> dict:
        """
        Get certificate history for an enrollment.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Certificate history
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/history/certificates"
        return self.get(path=path, headers={"accept": CERTIFICATE_HISTORY})

    def get_change_history(self, enrollment_id: int) -> dict:
        """
        Get change history for an enrollment.

        Args:
            enrollment_id: The enrollment ID

        Returns:
            Change history
        """
        path = f"/cps/v2/enrollments/{enrollment_id}/history/changes"
        return self.get(path=path, headers={"accept": CHANGE_HISTORY})
