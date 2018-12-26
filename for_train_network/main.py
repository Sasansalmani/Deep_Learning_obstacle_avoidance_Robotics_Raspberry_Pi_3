import load_data as LD
import create_network as CN
from sklearn.cross_validation import train_test_split

Num_epoch = 40

x, y = LD.load_data()
x_t, x_test, y_t, y_test = train_test_split(x, y, test_size=0.1, random_state=2)

CN.network(x_t, y_t, x_test, y_test, Num_epoch)

