

# Red Black Tree

#### 简介：

红黑树是一颗二叉搜索树。在每一个节点上添加一个存储位来表示节点颜色，可以是红色（RED）或者黑色（BLACK）。通过对任何一条从根到叶子的简单路径上各个节点的颜色进行约束，红黑树确保没有一条路径会比其他路径长出两倍，因而是<u>近似</u>于**平衡的。**



#### 红黑性质

1. 所有节点都是红色或者黑色。
2. 根节点是黑色
3. 叶子节点是黑色
4. 如果节点是红色，那么它的两个字节点都是黑色
5. 从任意节点的开始到其所有的叶子节点 ，所有的简单路径上的黑色节点个数相同



#### 树高

一棵有个`n` 个内部节点的红黑树，它的高度至多为 $2lg(n+1)$ 



#### 黑高：

从某一个节点 `x` 出发(不包含该节点)到达一个叶子节点的任意一条简单路径上的黑色节点个数称为该节点的黑高。



#### 旋转

我们在做 INSERT 和 UPDATE 操作时会破坏树的红黑性质，为了维护这些性质，我们需要改变树中某些节点的颜色和指针结构。

修改指针结构是通过**旋转**来完成的，这是一种能保持二叉搜索树性质的搜索树局部操作。

旋转分为两种：

- 左旋

  ```
  当y是x的右结点时得可用的旋转操作，x(父)结点变为y(右子)结点的左结点即为左旋，因为旋转需要保持树的平衡，所以y结点的左子树不变，而右结点指向x的右结点；x的右子树不变，左结点指向y的左结点，以此保证树的平衡。
  ```

  示例代码

  ```java
  //定义一个哨兵，用于表示叶子节点：哨兵节点为黑色，
  T.nil = new Node(Black);
  
  /** 
  	LEFT-ROTATION
  需要修改的节点指针：
  1.	x的父节点的left｜right指针 --->   y
  
  2. 	x的父指针 ---> y
  3.  x的左指针 ---> x.left
  4. 	x的右指针 ---> y.left
     
  5. 	y的父指针 ---> x.p
  6.  y的左指针 ---> x
  7.  y的右指针 ---> y.right
  */
  void leftRotation(BRTree t, Node x){
      Node y = x.left; //左旋即是与左节点交换，所以先找到左节点
      x.right = y.left;
      if(y.left != T.nil){
          y.left.p = x; //将原来的左节点接到x上。
      }
      y.p = x.p;
      if(x.p == T.nil ){ //如果x的父节点不存在，那么就设置y是树的root
          T.root = y;
      
      //如果x是左子节点，那么y替换x成为左子节点
      }else if (x == x.p.left){ 
          x.p.left = y;
      }else{ //同理，y替换x成为子字典
          x.p.right = y;
      }
      //x成为y的左子节点
      y.left = x;
      //y成为x的父节点
      x.p = y;
         
  }
  ```

  

- 右旋

  ```
  当y是x的左结点时得可用的旋转操作，x(父)结点变为y(右子)结点的右结点即为右旋，因为旋转需要保持树的平衡，所以y结点的右子树不变，而左结点指向x；x的左子树不变，x的右结点指向y的右结点，以此保证树的平衡
  ```

  ```java
  /** 
  RIGHT-ROTATION
  需要修改的节点指针：
  1.	x的父节点的left｜right指针 --->   y
  
  2. 	x的父指针 ---> y
  3.  x的左指针 ---> y.right
  4. 	x的右指针 ---> x.right
     
  5. 	y的父指针 ---> x.p  
  6.  y的左指针 ---> x
  7.  y的右指针 ---> y.right
  */
  void rightRatation(BRTree t , Node x){
      Node y = x.right; //右旋：与右节点交换位置。
      x.right = y.right;
      if(y.right != T.nil ){
          y.right.p = x;
      }else if(x == x.p.left){//设置父节点的子节点
          x.p.left = y; 
      }else{
          x.p.right = y ;
      }
      y.left = x;
      x.p = y
  }
  ```

  

#### Insert （插入）

我们可以在 $log_2(n)$ 时间内向一棵含有 $n$ 个节点的红黑树内插入一个红色的节点。为了能维持树的红黑性质，我们需要对红黑树内的节点做些一些调整。我们调用一个辅助程序`RB-INSERT-FIXUP`对节点重新着色和旋转，来保持红黑性质。

```java
/**
	BR-Tree-Insert
	与搜索树相同，我们需要把新节点插入到叶子
    遍历树，找到合适的位置
	修改新节点的父节点的左｜右指针
	修改新节点的父节点指针，
    修改新节点的左、右节点指向哨兵节点（T.nil）
*/
void insert(Tree t, Node z){
    Node y = T.nil;
    Node x = t.root;
    
    //遍历树
    while(x != T.nil){
        y = x ;				//保存遍历到的节点
        if(z.key < x.key ){
            x = x.left;		//x 向左下移动
        }else{
            x = x.right;	//x 向右下移动
        }
    }
    z.p = y;	   			//修改新节点的父指针
    if( y == T.nil){
        z = t.root;
    }else if (z.key < y.key){
        y.left = z; 		//父节点的左指针 指向 新节点
    }else{
        y.right = z;		//父节点的右指针  指向 新节点
    }
    z.left = T.nil;
    z.right = T.nil;
    z.color = Color.Red;	//设置为红色；（这里一定是设置为红色，后续解释）

    brTreeInsertFixup(t,z);	//插入后修复红黑树
}



```



###### RB-INSERT-FIXUP

我们向分析我们为什么需要调用修复方法来修复红黑树？

我们按搜索树的逻辑新添加了一个叶子节点，并把它着为红色,我们破坏了树的哪些红黑性质呢？

- 性质1：所有节点都是红色，或黑色。
  		我们插入了一个红色的节点，并没有破坏这条红黑性质。

- 性质2: 根节点是黑色。

  ​		如果树正好是一棵空树，那么我们插入一个红色节点后会破坏此条性质

- 性质3:叶子节点上黑色。
  	     我们所有的叶子节点都指向了哨兵节点，而哨兵都是黑色节点，所以此条性质不会被破坏

- 性质4:如果一个节点是红色，那么它的两个节点都是黑色。
      	我们插入一个红色的节点，如果新插入的节点的父节刚好是红色，那么此条性质会被破坏

- 性质5：任意节点到其所有叶子节点的简单路径上的黑色节点个数一致。

  ​		这是一条复杂的性质，在插入的算法中提到过，一定把新节点设置为红色，为的就是不破坏这一条性质。所以此条性质也不会被破坏。



所以我们总结一下，有可能被破坏的性质有：

	-	性质2 ：根节点是黑色。
	-	性质4：如果一个节点是红色，那么它的两个节点都是黑色。

我们继续分析如何修复这两种性质？ 

- 性质2:

  这条性质比较简单，我们可以在方法的最后直接修改根节点的颜色为黑色就可以修复。

  ```java
  t.root.color = BLACK;
  ```

  

- 性质4: 

  这条性质被破坏后的情况稍微有点复杂，我们一点一点的来分析。

  首先我们把目光先聚焦在 与新节点相关的几个节点上：

  - 新节点 z ： 				

  - z.p  z 的父节点          

  - z.p.p z 的祖父节点    

  - y z的叔节点               

    关于叔节点的选取，我们考虑如果这条性质被破坏，那么表示z 和 z.p 颜色都为红色，如果我们修复这种破坏，那么我们可能需要修改 z、z.p 和 z.p.p的颜色，那么就会影响到 y 节点，例如：我们修改 z.p 为黑色节点后，由于z.p.p是黑色节点，而如果此时y是红色(这是符合红黑性质的)，那么从z.p.p到z的黑色节点个数为2，然而另外一条从z.p.p到y的叶子节点简单路径的黑色节点个数为仅为1，这破坏了第5条性质。所以我们需要关注 y 的颜色情况。

  我们默认在我们插入 z  之前的红黑色树是维持着红黑性质的：我们先列举一下我们所关注的4个节点的颜色以及位置情况：

  | 名称 | color      | Position relative to gp (left of right)                      | Position relative to p (left of right) |
  | ---- | ---------- | ------------------------------------------------------------ | -------------------------------------- |
  | z    | red        | gp.left.left \| gp.left.right \| gp.right.left \| gp.right\|right | p.left \| p.right                      |
  | p    | red        | gp.left \| gp.right                                          | self                                   |
  | gp   | black      | self                                                         | p.p                                    |
  | y    | red｜black | gp.right \| gp.left                                          | p.p.left \| p.p.right                  |

  从上面的表格中我们发现，我们能确定的仅仅有z, p ,gp 的颜色，y的颜色以及它们相对于gp的位置关系是不清楚的，我们需要做旋转操作就比如弄清楚它们相对于gp的位置关系。

  结合上表以及性质4的描述，我们知道：

  1. 只有当p.color = RED 时红黑树的性质4才会被破坏。所以当p.color = Black时，我们不需要修复性质4.

  2. p相对于gp的位置可能是 left 或 right，根据二叉树的定义，y相对于gp的位置是与p 互斥。

  3. y的颜色可能为红色或黑色。

  4. z的位置比较复杂，依赖于 p 的情况。

     

  我们已经分析完我们需要关注的节点的情况，接下来我们分析会遇到的情况，以及如何修复：

  我们在这里在写一下出现一下情况的前提条件：

  ```java
  p.color = RED
  z.RED = RED
  z.p.p.color = BLACK
  ```

  1. p是gp的左节点， y是gp的右节点；
  2. p是gp的右节点，y是gp的左节点；
  3. z是p的左节点；
  4. z是p的右节点；
  5. y 的颜色是黑色；
  6. y 的颜色是红色；

  共6种情况，但有情况是对立的：整理后得：

  - y与p的颜色相同

    - z是p的左节点
      - p是gp的左节点
    - z是p的右节点
      - p是gp的右节点

  - y与p的颜色不同
    - p是gp的左节点

      - z是p的左节点

      - z是p的右节点

    - p是gp的右节点

      - z是p的左节点

      - z是p的右节点

  

  我们的目标是修复被破坏的性质4， 我们优先分析y与p的颜色是否相同带来的影响：

  - 相同：即同时为红色

    y与p颜色相同时，代表着我们仅需要通过修改节点颜色就可以维持红黑性质，我们需要分别修改3个节点的颜色：gp.color = RED、p.color = BLACK、y.color = BLACK。这样可以保证第5条性质不被破坏。同时也可以保证这部分子树维持性质4不被破坏，此时我们可以忽略节点之间的关系，因为我们不需要旋转。但有一个问题，我们修改了gp 的颜色为红色，我们需要把目光聚焦在gp上，再向上查看gp与gp.p 是否破坏的了性质4。所以我们把指针向上移动到gp。

    此部分的操作代码为：

    ```java
    gp.color = RED;
    p.color = BLACK;
    y.color = BLACK;
    z = gp;
    ```

  - 不同：即p.color = RED, y.color = BLACK

    y 与p的颜色不同时，不能通过简单的修改节点颜色的方式来修复被破坏的性质，

    原因有：

    1. 我们默认新节点加入前红黑树的性质都是可以维持的。我们可以用列举法来列举改变这几个节点可以能引起的情况：
       1. p.color = BLACK，将会破外性质5，gp的左子树与右子树下的黑高以一致，因为新增了一个黑节点。
       2. p.color = BLACK，y.color = RED。那么可能为会导致p.left.color = y.color = red。进一步都破坏了树的红黑树性质，甚至更难修复了。
       3. gp.color = RED ，p.color = BLACK。 同样会导致第5条性质被破坏。

    

    所以 我们需要通过旋转加修改颜色的方法修复被破坏的性质。

    我们先思考一下：我们要如何旋转，如何修改颜色呢？如何配合工作才能修复红黑性质呢？

    在回顾一下当前的情况：

    在新节点加入前红黑树是正常的，新节点加入后，性质4被破坏，

    gp.color = BLACK , y = BLACK, p.color = RED, z.color = RED;

    

    既然需要旋转，那么我们需要考虑到节点之间的相互位置。

    我们再深入思考一些：

    ​	我们需要把树通过旋转操作成什么样的结构才能保证红黑性质呢？

    	1. 同一层的节点的颜色都是一样的
    	2. 子节点与父节点都不一样。

    ​	节点间的关系对操作有什么影响吗？

    - z是p的左节点

      z.color = RED, p.color = RED, gp.color = BLACK , y.color = BLACK

      我们此时可以使用`rightRatation(gp)`，改变了几个节点的位置：

      - gp.p --> p;
      - gp.right --> y ; 
      - gp. left --> p.left;
      - p.right --> gp
      - p.left --> z

      我们发现此时z 和gp 成了同级，而y节点及其子树并不会收到影响。因此如果我们把 设置 gp 和 p的颜色 如下：

      -  gp.color = RED
      - p.color = BLACK

      此时的树的结构变为

      - p ---> root  , color = Black
        - z ---> p.left   , color = RED
        - gp --> p.right , color = RED 
          - y --> gp. child , color = BLACK

      这样的便完成了性质4的修复，且没有破坏其他性质。

      **示例代码**：

      ```java
      if(z == p.left){
          gp.color = RED;
          p.color = BLACK;
          rightRatation(t, gp)		//gp 与 p 的旋转
      }
      ```

      

    - z是p的右节点

      通过上面的分析，z是p的左节点时，我们通过一次右旋和改变gp、p的颜色即可完成修复。

      我们可以使用左旋将z 改变为p的左节点，再通过下一次循环完成修复

      具体操作如下：

      ```java
      if(z == p.right){
          z = p; //将指针上移，
      	leftRotation(t, z);
      }
      //指针上移后再通过左移后又被向下移动。又因为p和z 的颜色都是RED 所以并没有引起其他变化。
      ```

      

完整代码示例：

```java

/**
	红黑树插入后修复
*/
void brTreeInsertFixup(Tree t,Node z){
    while (z.p.color == Color.RED){				//
        if(z.p == z.p.p.left){					//
            Node y = z.p.p.right;
            if( y.color == Color.RED){			//颜色相同
                z.p.p.color = Color.RED;
                z.p.color = Color.BLACK;
                y.color = Color.BLACK;
                z = z.p.p;
            }else if(z == z.p.left){
                z.p.p.color = Color.RED;
                z.p.color = Color.BLACK;
                rightRatation(t, z.p.p)			//gp 与 p 的旋转
            }else{
                z = z.p; 						//将指针上移，
                leftRotation(t, z);  			//通过左旋造成z是左节点的情景
            }
        }else{
            Node y = z.p.p.left;
            if (y.color == Color.RED){
                z.p.p.color = Color.RED;
                z.p.color = Color.BLACK;
                y.color = Color.BLACk;
                z = z.p.p;
            }else if(z = z.p.right){
                z.p.p.color = Color.RED;
                z.p.color = Color.BLACK;
                leftRotation(t, z.p.p);
            }else{
                z = z.p;
                rightRatation(t, z);
            }
        }
    }
    t.root.color = Color.BLACk;
}
```

