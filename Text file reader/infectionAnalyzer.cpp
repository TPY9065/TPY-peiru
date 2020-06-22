//this is one of the two files that you need to submit

#include "infectionAnalyzer.h"
#include <fstream> //for reading file
#include <queue> //you may use STL queue
#include <algorithm> //you may use STL algorithm
using namespace std;
//you are NOT allowed to include additional libraries yourself

InfectionAnalyzer::~InfectionAnalyzer(){

	for (Tree<string>* tree: trees){
		delete tree;
	}
}

bool InfectionAnalyzer::loadInfectionFile(const string filename){
	fstream file;
	file.open(filename, ios::in);
	if (!file){	//the file cannot be loaded
		return false;
	}else{
		//cout << "File open successfully" << endl;
	}

	//cout << "Reading data from file..." << endl;
	// initialize the first tree


	while(!file.eof()){
		string parent;
		string child;
		file >> parent >> child;

		//cout << parent << " and " << child << endl;

		if (trees.empty()){	// the vector is empty
			Tree<string>* tree = new Tree<string>;
			//cout << "Trees is empty" << endl;
			tree->addRoot(parent);
			tree->addChild(parent, child);
			trees.push_back(tree);
		}else{
			//cout << "Trees is not empty" << endl;
			bool found = false;
			// found parent
			for (vector<Tree<string>*>::iterator it = trees.begin(); it != trees.end(); it++){
				if ((*it)->find(parent)){	// parent node is exist
					//cout << (*it)->root->data << " *it " << parent << endl;
					for (vector<Tree<string>*>::iterator st = trees.begin(); st != trees.end(); st++){
						if ((*st)->find(child)){
							//cout << (*st)->root->data << " *st " << child << endl;
							// find the parent position
							Tree<string>* tree = (*it)->find(parent);
							Tree<string>* new_tree_array = new Tree<string>[tree->root->childCount + 1];
							for (int i = 0; i < tree->root->childCount; i++){
								new_tree_array[i] = tree->root->children[i];
							}
							new_tree_array[tree->root->childCount] = (**st);
							delete (*st);
							delete []tree->root->children;
							tree->root->children = new_tree_array;
							tree->root->childCount += 1;
							trees.erase(st);
							found = true;
							break;
						}
					}
					if(!found){
						//cout << "not find " << child << endl;
						(*it)->addChild(parent, child);
						found = true;
					}
					break;
				}
			}

			if (found){
				continue;
			}
			// found child
			for (vector<Tree<string>*>::iterator it = trees.begin(); it != trees.end(); it++){
				if ((*it)->find(child)){	// child node is exist
					(*it)->addRoot(parent);
					found = true;
					break;
				}
			}

			if (found){
				continue;
			}

			Tree<string>* tree = new Tree<string>;
			//cout << "Trees is empty" << endl;
			tree->addRoot(parent);
			tree->addChild(parent, child);
			trees.push_back(tree);

		}

	}

	return true;
}

bool InfectionAnalyzer::isInfected(const string name) const{
	for(vector<Tree<string>*>::const_iterator it = trees.begin(); it != trees.end(); it++){
		if ((*it)->root->data == name){
			return true;
		}else{
			for (int i = 0; i < (*it)->root->childCount; i++){
				if ((*it)->root->children[i].find(name) != nullptr){
					return true;
				}
			}
		}
	}
	return false;
}

string InfectionAnalyzer::getInfectionSource(const string name) const{
	queue<Tree<string>*> nextTree;

	vector<Tree<string>*>::const_iterator it = trees.begin();
	nextTree.push(*it);
	Tree<string>* tree;

	while (!nextTree.empty() && it != trees.end()){
		tree = nextTree.back();
		nextTree.pop();

		if (tree->root->data == name){
			return "ZERO";
		}
		if (!(tree->find(name))){
			it += 1;
			nextTree.push(*it);
			continue;
		}else{
			bool exist = false;
			for (int i = 0; i < tree->root->childCount; i++){
				if (tree->root->children[i].find(name)){
					if (tree->root->children[i].root->data == name){
						return tree->root->data;
					}
					nextTree.push(tree->root->children + i);
					exist = true;
					break;
				}
			}
			if (!exist){
				if (it != trees.end()){
					it += 1;
					nextTree.push(*it);
				}
			}
		}
	}


	return "NA";
}

int InfectionAnalyzer::getInfectionGeneration(const string name) const{
	for (vector<Tree<string>*>::const_iterator it = trees.begin(); it != trees.end(); it++){
		if ((*it)->find(name) != nullptr){
			return (*it)->getDepth(name);
		}
	}
	return -1;
}

const vector<pair<string, int>>& InfectionAnalyzer::getInfectionPowerVector(){
	if (!infectionPowerVector.empty()){
		infectionPowerVector.clear();
	}


	vector<Tree<string>*>::const_iterator it = trees.begin();
	queue<Tree<string>*> nextTree;

	nextTree.push(*it);

	Tree<string>* tree;
	while(!nextTree.empty()){
		tree = nextTree.front();

		//cout << tree->root->data << endl;

		//cout << "Now the tree = " << nextTree.front()->root->data << endl;

		nextTree.pop();

		infectionPowerVector.push_back(make_pair(tree->root->data, tree->getDescendantCount()));

		//cout << "childCount of " << tree->root->data << " = " << tree->root->childCount << endl;

		for (int i = 0; i < tree->root->childCount; i++){
			/**
			if (tree->root->children[i].root->childCount > 0){

				//cout << "childCount > 0: " << tree->root->children[i].root->data << endl;

				nextTree.push((tree->root->children) + i);
			}else{

				//cout << "childCount = 0: " << tree->root->children[i].root->data << endl;

				string name = tree->root->children[i].root->data;
				int power = tree->root->children[i].getDescendantCount();
				infectionPowerVector.push_back(make_pair(name, power));
			}
			**/

			//cout << "The " << (i + 1) << " child of " << tree->root->data << " = " << (tree->root->children + i)->root->data << endl;

			Tree<string>* child = (tree->root->children + i);

			nextTree.push(child);

		}

		if (it + 1 != trees.end() && nextTree.empty()){
			it += 1;
			nextTree.push(*it);
		}
	}

	struct {
	  bool operator() (const pair<string, int>& a,const pair<string, int>& b) {
		  if (a.second == b.second){
			  return ( a.first < b.first );
		  }
		  return ( a.second > b.second );
	  }
	} order;

	sort(infectionPowerVector.begin(), infectionPowerVector.end(), order);

	return infectionPowerVector;

}

