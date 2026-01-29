from sklearn.linear_model import LinearRegression

X = [[1],[2],[3],[4]]
y = [30,50,70,150]
model = LinearRegression()
model.fit(X,y)
print(model.predict([[5]]))