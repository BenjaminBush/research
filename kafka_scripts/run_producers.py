import os
import multiprocessing
from periodic_producer import PeriodicProducer


def create_and_run(city):
	producer = PeriodicProducer(city)
	producer.run()





if __name__ == "__main__":
	process_idx = 0
	#cities = ['athens', 'east_rancho_dominguez', 'el_segundo', 'long_beach', 'lynwood', 'norwalk', 'redondo', 'wilmington']
	#cities = ['redondo', 'el_segundo']
	cities = ['redondo']
	for city in cities:
		p = multiprocessing.Process(target=create_and_run, args=(city,))
		os.system("taskset -p -c %d %d" % (process_idx % multiprocessing.cpu_count(), os.getpid()))
		process_idx += 1
		p.start()

