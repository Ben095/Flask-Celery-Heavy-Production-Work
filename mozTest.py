from mozscape import Mozscape, MozscapeError
client = Mozscape('member-79ea116cb0','43053334ef958fa5668a8afd8018195b')
Links = client.urlMetrics('https://www.benfolds.com/&sa=U&ved=0ahUKEwjSxZKtiP_PAhXIqFQKHaomCSsQFggsMAM&usg=AFQjCNGQFScP5dGElKPvz8zL1VyZvkQlxg',Mozscape.UMCols.pageAuthority | Mozscape.UMCols.mozRank | Mozscape.UMCols.links)
DA = client.urlMetrics('https://www.benfolds.com/',Mozscape.UMCols.domainAuthority)
print DA