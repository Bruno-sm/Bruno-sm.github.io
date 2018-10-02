#! /bin/python

import itertools
import time
from github import Github
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Devuelve un diccionario que asocia a cada lenguaje su número de repositorios
def count_repos_by_lang(repos):
	# Diccionario que guardará el número de repos por cada lenguaje
	repos_by_lang = {}

	for repo in repos:
		lang = repo.language
		if lang is None:
			continue
		# Si el lenguaje principal es Jupyter Notebook utilizamos el segundo más usado
		if lang == 'Jupyter Notebook':  
			languages = repo.get_languages()
			# En caso de que el único lenguaje sea Jupyter Notebook
			if len(languages) == 1:
				continue
			lang = sorted(languages, key=languages.get, reverse=True)[1]
		repos_by_lang[lang] = repos_by_lang.get(lang, 0) + 1

	return repos_by_lang


# Iniciamos sesión en GitHub
g = Github("usuario", "contraseña")

# Obtenemos los 500 repositorios más populares en inteligencia artificial
ai_repos = itertools.islice(g.search_repositories("artificial intelligence", sort="stars"), 500)
ai_repos_by_lang = count_repos_by_lang(ai_repos)

# Los disponemos en una gráfica
plt.bar(list(ai_repos_by_lang.keys()), list(ai_repos_by_lang.values()), color=(0.16, 0.5, 0.73, 1))
plt.xticks(rotation=90, fontsize='8')
plt.yticks(fontsize='8')
plt.subplots_adjust(bottom=0.2)
plt.show()

time.sleep(20)

# Obtenemos los 500 repositorios más populares de GitHub
popular_repos = itertools.islice(g.search_repositories("stars:>1", sort="stars"), 500)
popular_repos_by_lang = count_repos_by_lang(popular_repos)

# Calculamos el ratio de uso de cada lenguaje en proyectos de ia y en general
proportion_by_lang = {}
for lang in ai_repos_by_lang.keys():
	proportion_by_lang[lang] = ai_repos_by_lang[lang] / popular_repos_by_lang.get(lang, -1)

# Lo disponemos en una gráfica
plt.axes().yaxis.set_minor_locator(ticker.MultipleLocator(1))
plt.axhline(y=0, linewidth=0.75, color=(0.27, 0.27, 0.27))
plt.axhline(y=1, linewidth=0.35, color=(0.27, 0.27, 0.27))
plt.bar(list(proportion_by_lang.keys()), list(proportion_by_lang.values()), color=(0.16, 0.5, 0.73, 1))
plt.xticks(rotation=90, fontsize='8')
plt.yticks(fontsize='8')
plt.subplots_adjust(bottom=0.2)
plt.show()
