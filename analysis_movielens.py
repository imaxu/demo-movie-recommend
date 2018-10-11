# -*- coding : utf8 -*-
import pandas
import numpy
import warnings
#import matplotlib.pyplot as plt
#import seaborn as sb
warnings.filterwarnings("ignore")

def get_similar_data(ratingThreshold,movieTitle,top=10):
    # 读取并联合数据
    df = pandas.read_csv("ml-data/ratings.csv",sep=",")
    movie_titles = pandas.read_csv("ml-data/movies.csv",sep=",")
    df = pandas.merge(df,movie_titles,on="movieId")

    # 按电影标题统计投票数据
    ratings = pandas.DataFrame(df.groupby("title")["rating"].mean())
    # 增加一个投票数的列
    ratings["number_of_ratings"] = df.groupby("title")["rating"].count()

    #sb.jointplot(x="rating",y="number_of_ratings",data=ratings)

    # 将数据集转换为矩阵 
    movie_matrix = df.pivot_table(index="userId",columns="title",values="rating")
    #print(ratings.sort_values("number_of_ratings",ascending=False).head(10))

    # 在矩阵中查询相似度
    user_ratings = movie_matrix[movieTitle]
    similars = pandas.DataFrame(movie_matrix.corrwith(user_ratings),columns=["Correlation"])
    similars.dropna(inplace=True)
    corr = similars.join(ratings["number_of_ratings"])
    
    #plt.hist(ratings["rating"])
    #plt.show()
    #ratings["rating"].hist(bins=50)

    return corr[corr["number_of_ratings"]>ratingThreshold].sort_values(by="Correlation",ascending=False).head(top)

def main():
    print(get_similar_data(100,"Léon: The Professional (a.k.a. The Professional) (Léon) (1994)"))


if __name__ == '__main__':
    main()