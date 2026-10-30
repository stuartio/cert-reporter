from .base import Akamai
from typing import Optional, List


class AkamaiProperty(Akamai):
    # Contracts
    def list_contracts(self) -> list:
        """List all contracts."""
        path = "/papi/v1/contracts"
        result = self.get(path=path)
        return result["contracts"]["items"]

    # Groups
    def list_groups(self) -> list:
        """
        List all groups available to the user.

        Returns:
            List of groups
        """
        path = "/papi/v1/groups"
        result = self.get(path=path)
        return result["groups"]["items"]

    # Products
    def list_products(self, contract_id: str) -> list:
        """List products for a contract."""
        path = "/papi/v1/products"
        params = {"contractId": contract_id}
        result = self.get(path=path, params=params)
        return result["products"]["items"]

    # CP Codes
    def list_cp_codes(self, contract_id: str, group_id: str) -> list:
        """List CP codes."""
        path = "/papi/v1/cpcodes"
        params = {"contractId": contract_id, "groupId": group_id}
        result = self.get(path=path, params=params)
        return result["cpcodes"]["items"]

    def create_cp_code(self, contract_id: str, group_id: str, product_id: str, name: str) -> dict:
        """Create a new CP code."""
        path = "/papi/v1/cpcodes"
        params = {"contractId": contract_id, "groupId": group_id}
        body = {"productId": product_id, "cpcodeName": name}
        return self.post(path=path, params=params, body=body)

    def get_cp_code(self, cp_code_id: str, contract_id: str, group_id: str) -> dict:
        """Get CP code details."""
        path = f"/papi/v1/cpcodes/{cp_code_id}"
        params = {"contractId": contract_id, "groupId": group_id}
        result = self.get(path=path, params=params)
        return result["cpcodes"]["items"][0]

    # Edge Hostnames
    def list_edge_hostnames(self, contract_id: str, group_id: str) -> list:
        """List edge hostnames."""
        path = "/papi/v1/edgehostnames"
        params = {"contractId": contract_id, "groupId": group_id}
        result = self.get(path=path, params=params)
        return result["edgeHostnames"]["items"]

    def create_edge_hostname(
        self,
        contract_id: str,
        group_id: str,
        product_id: str,
        domain_prefix: str,
        domain_suffix: str,
        secure: bool = False,
        cert_enrollment_id: Optional[int] = None,
    ) -> dict:
        """Create a new edge hostname."""
        path = "/papi/v1/edgehostnames"
        params = {"contractId": contract_id, "groupId": group_id}
        body = {
            "productId": product_id,
            "domainPrefix": domain_prefix,
            "domainSuffix": domain_suffix,
            "secure": secure,
        }
        if cert_enrollment_id:
            body["certEnrollmentId"] = cert_enrollment_id
        return self.post(path=path, params=params, body=body)

    def get_edge_hostname(self, edge_hostname_id: str, contract_id: str, group_id: str) -> dict:
        """Get edge hostname details."""
        path = f"/papi/v1/edgehostnames/{edge_hostname_id}"
        params = {"contractId": contract_id, "groupId": group_id}
        result = self.get(path=path, params=params)
        return result["edgeHostnames"]["items"][0]

    # Properties
    def list_properties(self, contract_id: str, group_id: str) -> list:
        """List properties."""
        path = "/papi/v1/properties"
        params = {"contractId": contract_id, "groupId": group_id}
        result = self.get(path=path, params=params)
        return result["properties"]["items"]

    def create_property(
        self,
        contract_id: str,
        group_id: str,
        product_id: str,
        property_name: str,
        clone_from: Optional[dict] = None,
    ) -> dict:
        """Create a new property."""
        path = "/papi/v1/properties"
        params = {"contractId": contract_id, "groupId": group_id}
        body = {"productId": product_id, "propertyName": property_name}
        if clone_from:
            body["cloneFrom"] = clone_from
        return self.post(path=path, params=params, body=body)

    def get_property(self, property_id: str) -> dict:
        """
        Get property details.

        Args:
            property_id: The property ID

        Returns:
            Property details
        """
        path = f"/papi/v1/properties/{property_id}"
        result = self.get(path=path)
        return result["properties"]["items"][0]

    def delete_property(self, property_id: str) -> dict:
        """Delete a property."""
        path = f"/papi/v1/properties/{property_id}"
        return self.delete(path=path)

    # Property Versions
    def list_property_versions(self, property_id: str) -> list:
        """List all versions for a property."""
        path = f"/papi/v1/properties/{property_id}/versions"
        result = self.get(path=path)
        return result["versions"]["items"]

    def new_property_version(self, property_id: str, create_from_version: int) -> str:
        """
        Create a new property version.

        Args:
            property_id: The property ID
            create_from_version: Version to create from

        Returns:
            Link to the new version
        """
        path = f"/papi/v1/properties/{property_id}/versions"
        data = {"createFromVersion": create_from_version}
        result = self.post(path=path, body=data)
        return result["versionLink"]

    def get_property_version(self, property_id: str, version: int) -> dict:
        """Get property version details."""
        path = f"/papi/v1/properties/{property_id}/versions/{version}"
        result = self.get(path=path)
        return result["versions"]["items"][0]

    def get_latest_version(self, property_id: str, activate_on: str = "STAGING") -> dict:
        """Get latest property version."""
        path = f"/papi/v1/properties/{property_id}/versions/latest"
        params = {"activatedOn": activate_on}
        result = self.get(path=path, params=params)
        return result["versions"]["items"][0]

    def delete_property_version(self, property_id: str, version: int) -> dict:
        """Delete a property version."""
        path = f"/papi/v1/properties/{property_id}/versions/{version}"
        return self.delete(path=path)

    # Property Hostnames
    def list_hostnames(self, property_id: str, version: int) -> list:
        """
        List hostnames for a property version.

        Args:
            property_id: The property ID
            version: The property version

        Returns:
            List of hostnames
        """
        path = f"/papi/v1/properties/{property_id}/versions/{version}/hostnames"
        result = self.get(path=path)
        return result["hostnames"]["items"]

    def set_hostnames(self, property_id: str, version: int, hostnames: list) -> dict:
        """
        Set hostnames for a property version.

        Args:
            property_id: The property ID
            version: The property version
            hostnames: List of hostname configurations

        Returns:
            Updated hostnames response
        """
        path = f"/papi/v1/properties/{property_id}/versions/{version}/hostnames"
        return self.put(path=path, body=hostnames)

    # Account Hostnames
    def list_account_hostnames(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        contract_id: Optional[str] = None,
        group_id: Optional[str] = None,
        network: Optional[str] = None,
        hostname: Optional[str] = None,
        cname_to: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> list:
        """
        List hostnames for the account.

        By default all pages are retrieved. If page or page_size is specified, only that
        single page is returned. The API pages with offset/limit; offset is derived as
        (page - 1) * page_size.

        Args:
            page: 1-based page number (defaults to 1 when only page_size is given)
            page_size: Number of hostnames per page (defaults to 999 when only page is given)
            contract_id: Filter by contract ID
            group_id: Filter by group ID
            network: Filter by network ('PRODUCTION' or 'STAGING')
            hostname: Filter by cnameFrom, supports '*' wildcards
            cname_to: Filter by edge hostname, supports '*' wildcards
            sort: 'hostname:a' (ascending) or 'hostname:d' (descending)

        Returns:
            List of hostnames
        """
        path = "/papi/v1/hostnames"
        headers = {"PAPI-Use-Prefixes": "false"}
        params = {
            "contractId": contract_id,
            "groupId": group_id,
            "network": network,
            "hostname": hostname,
            "cnameTo": cname_to,
            "sort": sort,
        }
        params = {k: v for k, v in params.items() if v is not None}

        if page is not None or page_size is not None:
            page = 1 if page is None else page
            page_size = 999 if page_size is None else page_size
            if page < 1 or page_size < 1:
                raise ValueError("page and page_size must be >= 1")
            params["offset"] = (page - 1) * page_size
            params["limit"] = page_size
            result = self.get(path=path, params=params, headers=headers)
            return result["hostnames"]["items"]

        limit = 999
        offset = 0
        items: list = []
        while True:
            result = self.get(path=path, params={**params, "offset": offset, "limit": limit}, headers=headers)
            page_items = result["hostnames"]["items"]
            items.extend(page_items)
            offset += len(page_items)
            if not page_items or offset >= result["hostnames"]["totalItems"]:
                break
        return items

    # Property Rules
    def get_property_rules(self, property_id: str, property_version: int, rule_format: Optional[str] = None) -> dict:
        """
        Get property rules for a specific version.

        Args:
            property_id: The property ID
            property_version: The property version
            rule_format: Optional rule format version (e.g., 'v2023-01-05')

        Returns:
            Property rules
        """
        path = f"/papi/v1/properties/{property_id}/versions/{property_version}/rules"
        headers = {}
        if rule_format is not None:
            headers["Accept"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.get(path=path, headers=headers)

    def update_version(
        self,
        property_id: str,
        property_version: int,
        rules: dict,
        rule_format: Optional[str] = None,
    ) -> dict:
        """
        Update property rules for a version.

        Args:
            property_id: The property ID
            property_version: The property version
            rules: Rules configuration
            rule_format: Optional rule format version (e.g., 'v2023-01-05')

        Returns:
            Update response
        """
        path = f"/papi/v1/properties/{property_id}/versions/{property_version}/rules"
        headers = {}
        if rule_format is not None:
            headers["Content-Type"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.put(path=path, headers=headers, body=rules)

    def validate_rules(self, property_id: str, property_version: int, rule_format: Optional[str] = None) -> dict:
        """Validate property rules."""
        path = f"/papi/v1/properties/{property_id}/versions/{property_version}/rules/validate-mode"
        headers = {}
        if rule_format is not None:
            headers["Accept"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.get(path=path, headers=headers)

    def digest_property_rules(self, property_id: str, version: int) -> dict:
        """Get property rules digest."""
        path = f"/papi/v1/properties/{property_id}/versions/{version}/rules/digest"
        return self.get(path=path)

    # Property Activations
    def list_activations(self, property_id: str) -> list:
        """
        List activations for a property.

        Args:
            property_id: The property ID

        Returns:
            List of activations
        """
        path = f"/papi/v1/properties/{property_id}/activations"
        result = self.get(path=path)
        return result["activations"]["items"]

    def activate(
        self,
        property_id: str,
        property_version: int,
        network: str,
        email_addresses: List[str],
        notes: Optional[str] = None,
    ) -> dict:
        """
        Activate a property version.

        Args:
            property_id: The property ID
            property_version: The property version to activate
            network: Network to activate on ('staging' or 'production')
            email_addresses: List of email addresses for notifications
            notes: Optional activation notes

        Returns:
            Activation response
        """
        path = f"/papi/v1/properties/{property_id}/activations"
        data = {
            "acknowledgeAllWarnings": True,
            "activationType": "ACTIVATE",
            "network": network,
            "notifyEmails": email_addresses,
            "note": notes,
            "propertyVersion": property_version,
        }
        return self.post(path=path, body=data)

    def get_activation(self, property_id: str, activation_id: str) -> dict:
        """Get activation details."""
        path = f"/papi/v1/properties/{property_id}/activations/{activation_id}"
        result = self.get(path=path)
        return result["activations"]["items"][0]

    def cancel_activation(self, property_id: str, activation_id: str) -> dict:
        """Cancel a pending activation."""
        path = f"/papi/v1/properties/{property_id}/activations/{activation_id}"
        return self.delete(path=path)

    def deactivate_property(
        self,
        property_id: str,
        property_version: int,
        network: str,
        email_addresses: List[str],
        notes: Optional[str] = None,
    ) -> dict:
        """Deactivate a property."""
        path = f"/papi/v1/properties/{property_id}/activations"
        data = {
            "acknowledgeAllWarnings": True,
            "activationType": "DEACTIVATE",
            "network": network,
            "notifyEmails": email_addresses,
            "note": notes,
            "propertyVersion": property_version,
        }
        return self.post(path=path, body=data)

    # Includes
    def list_includes(self, contract_id: str, group_id: str) -> list:
        """List includes."""
        path = "/papi/v1/includes"
        params = {"contractId": contract_id, "groupId": group_id}
        result = self.get(path=path, params=params)
        return result["includes"]["items"]

    def create_include(
        self,
        contract_id: str,
        group_id: str,
        product_id: str,
        include_name: str,
        include_type: str = "MICROSERVICES",
    ) -> dict:
        """Create a new include."""
        path = "/papi/v1/includes"
        params = {"contractId": contract_id, "groupId": group_id}
        body = {
            "productId": product_id,
            "includeName": include_name,
            "includeType": include_type,
        }
        return self.post(path=path, params=params, body=body)

    def get_include(self, include_id: str) -> dict:
        """Get include details."""
        path = f"/papi/v1/includes/{include_id}"
        result = self.get(path=path)
        return result["includes"]["items"][0]

    def delete_include(self, include_id: str) -> dict:
        """Delete an include."""
        path = f"/papi/v1/includes/{include_id}"
        return self.delete(path=path)

    def list_include_versions(self, include_id: str) -> list:
        """List versions for an include."""
        path = f"/papi/v1/includes/{include_id}/versions"
        result = self.get(path=path)
        return result["versions"]["items"]

    def create_include_version(self, include_id: str, create_from_version: int) -> dict:
        """Create a new include version."""
        path = f"/papi/v1/includes/{include_id}/versions"
        body = {"createFromVersion": create_from_version}
        return self.post(path=path, body=body)

    def get_include_rules(self, include_id: str, version: int, rule_format: Optional[str] = None) -> dict:
        """Get include rules."""
        path = f"/papi/v1/includes/{include_id}/versions/{version}/rules"
        headers = {}
        if rule_format:
            headers["Accept"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.get(path=path, headers=headers)

    def update_include_rules(
        self, include_id: str, version: int, rules: dict, rule_format: Optional[str] = None
    ) -> dict:
        """Update include rules."""
        path = f"/papi/v1/includes/{include_id}/versions/{version}/rules"
        headers = {}
        if rule_format:
            headers["Content-Type"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.put(path=path, headers=headers, body=rules)

    def list_include_activations(self, include_id: str) -> list:
        """List include activations."""
        path = f"/papi/v1/includes/{include_id}/activations"
        result = self.get(path=path)
        return result["activations"]["items"]

    def activate_include(
        self,
        include_id: str,
        version: int,
        network: str,
        email_addresses: List[str],
        notes: Optional[str] = None,
    ) -> dict:
        """Activate an include version."""
        path = f"/papi/v1/includes/{include_id}/activations"
        data = {
            "acknowledgeAllWarnings": True,
            "activationType": "ACTIVATE",
            "network": network,
            "notifyEmails": email_addresses,
            "note": notes,
            "includeVersion": version,
        }
        return self.post(path=path, body=data)

    # Rule Formats and Schemas
    def list_rule_formats(self) -> list:
        """List available rule formats."""
        path = "/papi/v1/rule-formats"
        result = self.get(path=path)
        return result["ruleFormats"]["items"]

    def get_rule_format_schema(self, product_id: str, rule_format: str) -> dict:
        """Get schema for a rule format."""
        path = f"/papi/v1/schemas/products/{product_id}/{rule_format}"
        return self.get(path=path)

    def get_available_criteria(self, property_id: str, version: int, rule_format: Optional[str] = None) -> dict:
        """Get available criteria for a property version."""
        path = f"/papi/v1/properties/{property_id}/versions/{version}/available-criteria"
        headers = {}
        if rule_format:
            headers["Accept"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.get(path=path, headers=headers)

    def get_available_behaviors(self, property_id: str, version: int, rule_format: Optional[str] = None) -> dict:
        """Get available behaviors for a property version."""
        path = f"/papi/v1/properties/{property_id}/versions/{version}/available-behaviors"
        headers = {}
        if rule_format:
            headers["Accept"] = f"application/vnd.akamai.papirules.{rule_format}+json"
        return self.get(path=path, headers=headers)

    # Search and Bulk Operations
    def find_property(self, property_name: str) -> list:
        """
        Find property by name.

        Args:
            property_name: Name of the property to find

        Returns:
            List of matching property versions
        """
        path = "/papi/v1/search/find-by-value"
        data = {"propertyName": property_name}
        result = self.post(path=path, body=data)
        return result["versions"]["items"]

    def bulk_search(self, search_data: dict) -> list:
        """
        Perform bulk rules search across properties.

        Args:
            search_data: Search criteria

        Returns:
            Search results
        """
        path = "/papi/v1/bulk/rules-search-requests-synch"
        result = self.post(path=path, body=search_data)
        return result["results"]

    def bulk_activate(self, activation_data: dict) -> dict:
        """Bulk activate properties."""
        path = "/papi/v1/bulk/activations"
        return self.post(path=path, body=activation_data)

    def bulk_patch_properties(self, patch_data: dict) -> dict:
        """Bulk patch properties."""
        path = "/papi/v1/bulk/property-version-creations"
        return self.post(path=path, body=patch_data)

    def bulk_version_create(self, version_data: dict) -> dict:
        """Bulk create property versions."""
        path = "/papi/v1/bulk/property-version-creations"
        return self.post(path=path, body=version_data)
