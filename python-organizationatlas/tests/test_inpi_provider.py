"""INPI provider API path tests."""

from unittest.mock import MagicMock, patch

from organizationatlas.providers.europe.france.inpi import InpiProvider


class TestInpiProviderApiPaths:
    @patch.object(InpiProvider, "_get_token", return_value="token")
    @patch("organizationatlas.providers.europe.france.inpi.requests.get")
    def test_search_uses_companies_endpoint(self, mock_get, _mock_token):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"companies": [{"siren": "917432254"}]},
        )
        mock_get.return_value.raise_for_status = MagicMock()

        provider = InpiProvider()
        with patch.object(
            provider,
            "search_organization_by_reference",
            return_value={
                "siren": "917432254",
                "content": {
                    "personneMorale": {
                        "identite": {"entreprise": {"denomination": "OCTOLO"}},
                    },
                },
            },
        ):
            results = provider.search_organization("octolo")

        assert len(results) == 1
        mock_get.assert_called_once()
        url = mock_get.call_args[0][0]
        params = mock_get.call_args[1]["params"]
        assert url.endswith("/api/companies")
        assert params["companyName"] == "octolo"
        assert "organizationName" not in params

    @patch.object(InpiProvider, "_get_token", return_value="token")
    @patch("organizationatlas.providers.europe.france.inpi.requests.get")
    def test_search_by_reference_uses_companies_siren(self, mock_get, _mock_token):
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"siren": "917432254"},
        )
        mock_get.return_value.raise_for_status = MagicMock()

        provider = InpiProvider()
        result = provider.search_organization_by_reference("917432254")

        assert result == {"siren": "917432254"}
        mock_get.assert_called_once()
        assert mock_get.call_args[0][0].endswith("/api/companies/917432254")

    def test_normalize_denomination_from_content(self):
        provider = InpiProvider()
        data = {
            "siren": "917432254",
            "content": {
                "personneMorale": {
                    "identite": {"entreprise": {"denomination": "OCTOLO"}},
                },
            },
        }
        normalized = provider.normalize(data, config=provider.services_cfg["search_organization"])
        assert normalized["denomination"] == "OCTOLO"
        assert normalized["reference"] == "917432254"

    def test_normalize_reference_prefers_siret_over_siren(self):
        provider = InpiProvider()
        data = {
            "siren": "917432254",
            "formality": {
                "content": {
                    "personneMorale": {
                        "etablissementPrincipal": {
                            "descriptionEtablissement": {
                                "siret": "91743225400014",
                            },
                        },
                    },
                },
            },
        }

        normalized = provider.normalize(data, config=provider.services_cfg["search_organization"])

        assert normalized["reference"] == "91743225400014"
        assert normalized["source_field"] == "siret"

    def test_normalize_ape_from_inpi_code_uses_referentiel_format(self):
        provider = InpiProvider()
        data = {
            "siren": "917432254",
            "formality": {
                "content": {
                    "personneMorale": {
                        "identite": {"entreprise": {"codeApe": "6201Z"}},
                    },
                },
            },
        }

        normalized = provider.normalize(data, config=provider.services_cfg["search_organization"])

        assert normalized["ape"] == "62.01Z"

    def test_normalize_denomination_personne_physique_autres_etablissements(self):
        provider = InpiProvider()
        data = {
            "siren": "977793561",
            "content": {
                "personnePhysique": {
                    "identite": {
                        "entreprise": None,
                        "entrepreneur": {
                            "descriptionPersonne": {
                                "nom": "ZLAIJI EL BAZAZI",
                                "prenoms": ["MOHAMMED"],
                            },
                        },
                    },
                    "etablissementPrincipal": None,
                    "autresEtablissements": [
                        {
                            "descriptionEtablissement": {
                                "indicateurEtablissementPrincipal": True,
                                "nomCommercial": "DOCTOLOC",
                            },
                        },
                    ],
                },
            },
        }
        normalized = provider.normalize(data, config=provider.services_cfg["search_organization"])
        assert normalized["denomination"] == "DOCTOLOC"
        assert normalized["reference"] == "977793561"
