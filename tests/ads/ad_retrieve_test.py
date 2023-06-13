import pytest

from ads.serializers import AdListSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_retrieve_ad(client, member_token):
    ad = AdFactory.create()

    expected_response = AdListSerializer(ad).data

    response = client.get(
        f"/ad/{ad.pk}/",
        HTTP_AUTHORIZATION="Bearer " + member_token
    )

    assert response.status_code == 200
    assert response.data == expected_response
