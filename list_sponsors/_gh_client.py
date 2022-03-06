import json
from textwrap import dedent
from typing import Dict, Iterator, Optional, Union

import retryrequests

from ._logger import logger
from ._sponsor import Sponsor


class GitHubV4Client:
    def __init__(self, token: str) -> None:
        self.__token = token

    def exec_query(
        self, query: str, variables: Optional[Dict[str, Union[str, int]]] = None
    ) -> Dict:
        logger.debug(f"[query]\n{dedent(query).strip()}\n")
        if variables:
            logger.debug(f"[variables]\n{json.dumps(variables, indent=2)}\n")

        r = retryrequests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers={"Authorization": f"Bearer {self.__token}"},
        )
        r.raise_for_status()

        results = r.json()
        logger.debug(f"[results]\n{json.dumps(results, indent=2)}\n")

        return results

    def fetch_login_user_name(self) -> str:
        result = self.exec_query("{ viewer { login } }")

        return result["data"]["viewer"]["login"]

    def __fetch_sponsors(self, login: str, after: str, avatar_size: int) -> Dict:
        assert login

        common_query = """
                    sponsorshipsAsMaintainer(first: $first, after: $after) {
                        totalCount
                        pageInfo {
                            hasNextPage
                            hasPreviousPage
                            startCursor
                            endCursor
                        }
                        edges {
                            cursor
                            node {
                                isOneTimePayment
                                privacyLevel
                                createdAt
                                tier {
                                    name
                                    monthlyPriceInDollars
                                }
                                sponsorEntity {
                                    ... on User {
                                        name
                                        login
                                        avatarUrl(size: $avatar_size)
                                        url
                                    }
                                }
                            }
                        }
                    }"""
        query = (
            """\
            query($login: String!, $avatar_size: Int!, $first: Int!, $after: String!) {
                user(login: $login) {"""
            + common_query
            + """
                }
                """
            + """

                organization(login: $login) {"""
            + common_query
            + """
                }
            }
            """
        )
        variables: Dict[str, Union[str, int]] = {
            "login": login,
            "first": 100,
            "after": after,
            "avatar_size": avatar_size,
        }
        result = self.exec_query(query, variables=variables)

        if result["data"]["user"]:
            return result["data"]["user"]["sponsorshipsAsMaintainer"]
        elif result["data"]["organization"]:
            return result["data"]["organization"]["sponsorshipsAsMaintainer"]

        raise RuntimeError("empty result")

    def fetch_sponsors(self, login: str, avatar_size: int) -> Iterator[Sponsor]:
        sponsorships = self.__fetch_sponsors(login=login, after="", avatar_size=avatar_size)
        logger.debug(f"results - totalCount: {sponsorships['totalCount']}")

        for sponsor in sponsorships["edges"]:
            node = sponsor["node"]
            entity = node["sponsorEntity"]
            if not entity:
                continue

            tier = node["tier"]
            if not tier:
                price = None
            else:
                price = tier["monthlyPriceInDollars"] if "monthlyPriceInDollars" in tier else None
                # print(price)

            yield Sponsor(
                **entity, monthlyPriceInDollars=price, isOneTimePayment=node["isOneTimePayment"]
            )

        page_info = sponsorships["pageInfo"]
        # print(page_info)

        while page_info["hasNextPage"]:
            sponsorships = self.__fetch_sponsors(
                login=login, after=page_info["endCursor"], avatar_size=avatar_size
            )
            for sponsor in sponsorships["edges"]:
                node = sponsor["node"]
                entity = node["sponsorEntity"]
                if not entity:
                    continue

                tier = node["tier"]
                if not tier:
                    price = None
                else:
                    price = (
                        tier["monthlyPriceInDollars"] if "monthlyPriceInDollars" in tier else None
                    )

                yield Sponsor(
                    **entity, monthlyPriceInDollars=price, isOneTimePayment=node["isOneTimePayment"]
                )

            page_info = sponsorships["pageInfo"]
            # print(page_info)
