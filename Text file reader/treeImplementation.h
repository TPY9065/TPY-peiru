//this is one of the two files that you need to submit

using namespace std;
//you are NOT allowed to include additional libraries yourself

//you do NOT need to include "tree.h" in this file
//this is NOT a cpp file, but simply a part of "tree.h"
//see the bottom of tree.h for explanation
//just write your tree implementation here right away
template <typename T>
Tree<T>::Tree(const Tree<T>& another){
	if (another.isEmpty()){

		//cout << "another is empty" << endl;

		return;
	}else{
		delete root;
		root = new Node<T>(*(another.root));
	}

	//cout << "Finish" << endl;
}

template <typename T>
Tree<T>::~Tree(){
	delete root;
}

template <typename T>
const Tree<T>& Tree<T>::operator= (const Tree<T>& another){
	if (this == &another){
		return *this;
	}
	if (another.isEmpty()){
		delete root;
		root = nullptr;
		return *this;
	}
	delete root;
	root = new Node<T>(*another.root);
	return *this;
}

template <typename T>
Tree<T>* Tree<T>::find(const T& data){
	if (root == nullptr){
		return nullptr;
	}else if (root->data == data){
		return this;
	}else if (root->data != data){

		Tree* target = nullptr;

		for (int i = 0; i < root->childCount; i++){
			target = (root->children[i]).find(data);
			if (target != nullptr){
				return target;
			}
		}
	}
	return nullptr;
}

template <typename T>
const Tree<T>* Tree<T>::find(const T& data) const{
	if (root == nullptr){
		return nullptr;
	}else if (root->data == data){
		return this;
	}else if (root->data != data){

		Tree* target = nullptr;

		for (int i = 0; i < root->childCount; i++){
			target = (root->children[i]).find(data);
			if (target != nullptr){
				return target;
			}
		}
	}
	return nullptr;
}

template <typename T>
int Tree<T>::getDepth(const T& data) const{
	if (root->data == data){
		return 0;
	}
	if (isEmpty() || find(data) == nullptr){
		return -1;
	}
	int depth = 0;
	for (int i = 0; i < root->childCount; i++){
		depth += (root->children[i]).getDepth(data) + 1;
	}
	return depth;
}

template <typename T>
int Tree<T>::getDescendantCount(const T& data) const{
	const Tree<T>* target = this->find(data);
	if (target == nullptr || target->isEmpty()){
		return -1;
	}
	return target->getDescendantCount();
}

template <typename T>
int Tree<T>::getDescendantCount() const{
	if (isEmpty()){
		return -1;
	}
	int count = 0;
	for (int i = 0; i < root->childCount; i++){
		if (root->children[i].root->childCount != 0){
			count += (root->children[i]).getDescendantCount() + 1;
		}else{
			count += 1;
		}
	}
	return count;
}

template <typename T>
bool Tree<T>::addRoot(const T& data){
	if (isEmpty()){

		//cout << "The tree is empty." << endl;

		root = new Node<T>(data);
		return true;
	}else{

		Tree* target = find(data);

		if (target != nullptr){

			//cout << "The node is already exist." << endl;

			return false;
		}

		//cout << "The tree is not empyt." << endl;

		if (root != nullptr){
			Node<T>* new_node = new Node<T>(data, 1);
			new_node->children[0] = *this;
			delete root;
			root = new_node;
			return true;
		}else{
			root = new Node<T>(data);
			return true;
		}
	}
}

template <typename T>
bool Tree<T>::addChild(const T& parentData, const T& childData){
	Tree<T>* target = find(parentData);

	if (target == nullptr){

		//cout << "The parent node is not found." << endl;

		return false;
	}

	//cout << target->root->data << target->root->childCount << endl;
	//cout << (target->root->children != nullptr) << endl;

	//cout << "Initializing new tree..., the parent node is: " << target->root->data
	//	 << " The childCount: " << target->root->childCount << endl;

	Tree<T>* new_children_array = new Tree<T>[target->root->childCount + 1];

	//cout << target->root->childCount << endl;

	for (int i = 0; i < target->root->childCount; i++){
		new_children_array[i] = target->root->children[i];
	}

	//cout << "Finish assigning old trees to new tree." << endl;


	new_children_array[target->root->childCount] = Tree<T>();
	new_children_array[target->root->childCount].root = new Node<T>(childData);


	if (target->root->children != nullptr){
		delete []target->root->children;
	}

	target->root->children = new_children_array;

	target->root->childCount += 1;

	return true;
}
