import aiohttp

airing_query = '''
    query ($id: Int,$search: String) { 
        Media (id: $id, type: ANIME,search: $search) { 
            id
            episodes
            title {
                romaji
                english
                native
            }
            nextAiringEpisode {
                airingAt
                timeUntilAiring
                episode
            } 
        }
    }
    '''

fav_query = """
query ($id: Int) { 
    Media (id: $id, type: ANIME) { 
        id
        title {
            romaji
            english
            native
        }
    }
}
"""

anime_query = '''
query ($search: String) {
  Page(page: 1, perPage: 30) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media(search: $search, type: ANIME) {
      id
      title {
        romaji
        english
        native
      }
      description(asHtml: false)
      startDate {
        year
      }
      episodes
      season
      type
      format
      status
      duration
      siteUrl
      studios {
        nodes {
          name
        }
      }
      trailer {
        id
        site
        thumbnail
      }
      averageScore
      genres
      coverImage{
        medium
      }
    }
  }
}
'''
character_query = """
    query ($query: String) {
        Character (search: $query) {
            id
            name {
                first
                last
                full
            }
            siteUrl
            image {
                large
            }
            description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) { 
    Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
            romaji
            english
            native
        }
        description (asHtml: false)
        startDate{
            year
        }
        type
        format
        status
        siteUrl
        averageScore
        genres
        bannerImage
    }
}
"""

anime_search_query = """
query ($search: String, $page: Int, $id:[Int]) {
  Page(page: $page, perPage: 1) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media(search: $search, type: ANIME, id_in: $id) {
      id
      title {
        romaji
        english
        native
      }
      description(asHtml: false)
      startDate {
        year
      }
      episodes
      season
      type
      format
      status
      duration
      siteUrl
      studios {
        nodes {
          name
        }
      }
      trailer {
        id
        site
        thumbnail
      }
      averageScore
      genres
      coverImage {
        medium
      }
      isAdult
      hashtag
    }
  }
}
"""

url = 'https://graphql.anilist.co'


async def airing_sauce(query):
    variables = {'search': query}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': airing_query, 'variables': variables}
        ) as resp:
            return await resp.json()


async def fav_sauce(query):
    variables = {'search': query}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': fav_query, 'variables': variables}
        ) as resp:
            return await resp.json()


async def anime_sauce(query):
    variables = {'search': query}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': anime_query, 'variables': variables}
        ) as resp:
            return await resp.json()


async def anime_search(query, page):
    variables = {'search': query, 'page': page}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={"query": anime_search_query, 'variables': variables}
        ) as resp:
            return await resp.json()


async def get_anime(id):
    variables = {'id': id, 'page': 1}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={"query": anime_search_query, 'variables': variables}
        ) as resp:
            return await resp.json()


async def character_sauce(query):
    variables = {'search': query}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': character_query, 'variables': variables}
        ) as resp:
            return await resp.json()


async def manga_sauce(query):
    variables = {'search': query}
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            url, json={'query': manga_query, 'variables': variables}
        ) as resp:
            return await resp.json()
