//
// Created by Dominika on 30.09.2020.
//

#ifndef IMPLEMENTATION_TSP_HPP
#define IMPLEMENTATION_TSP_HPP

#include <vector>
#include <numeric>
#include <ostream>

#include "tsp_setup.hpp"

using cost_matrix_t = std::vector<std::vector<cost_t>>;

struct vertex_t {
    std::size_t row;
    std::size_t col;
    vertex_t(std::size_t r = 0, std::size_t c = 0) : row(r), col(c) {}
};

using unsorted_path_t = std::vector<vertex_t>;

struct tsp_solution_t {
    cost_t lower_bound;
    path_t path;
};

using tsp_solutions_t = std::vector<tsp_solution_t>;

struct NewVertex {
    NewVertex(vertex_t v = {}, cost_t cost = 0) : coordinates(v), cost(cost) {}

    vertex_t coordinates;
    cost_t cost;
};

class CostMatrix {
public:
    CostMatrix(cost_matrix_t m = {}) : matrix_(m) {}

    std::size_t size() const { return matrix_.size(); }

    const std::vector<cost_t>& operator[](std::size_t pos) const { return matrix_[pos]; }
    std::vector<cost_t>& operator[](std::size_t pos) { return matrix_[pos]; }

    const cost_matrix_t& get_matrix() const { return matrix_; };

    cost_t reduce_rows();
    cost_t reduce_cols();

    std::vector<cost_t> get_min_values_in_rows() const;
    std::vector<cost_t> get_min_values_in_cols() const;

    cost_t get_vertex_cost(std::size_t row, std::size_t col) const;

private:
    cost_matrix_t matrix_;
};

std::ostream& operator<<(std::ostream& os, const CostMatrix& cm);

/**
 * The <tt>StageState</tt> class stores information about the partial solution
 * at the given stage.
 */
class StageState : public IStageState {
public:


    StageState(const CostMatrix& m, std::vector<vertex_t> p = {},
            cost_t lb = 0) : matrix_(m), unsorted_path_(p), lower_bound_(lb) {};

    path_t get_path();
    std::size_t get_level() const { return unsorted_path_.size(); }

    void update_lower_bound(cost_t reduced_values) { lower_bound_ += reduced_values; }
    cost_t get_lower_bound() const { return lower_bound_; }
    void reset_lower_bound() { lower_bound_ = 0; }

    const CostMatrix& get_matrix() const { return matrix_; };
    const unsorted_path_t& get_unsorted_path() const { return unsorted_path_; }
    void append_to_path(const vertex_t& v) { unsorted_path_.push_back(v); }

    cost_t reduce_cost_matrix();
    NewVertex choose_new_vertex();
    void update_cost_matrix(vertex_t new_vertex);

private:
    CostMatrix matrix_;
    unsorted_path_t unsorted_path_;
    cost_t lower_bound_;
};

//NewVertex choose_new_vertex(const CostMatrix& cm);
cost_t get_optimal_cost(const path_t& optimal_path, const cost_matrix_t& m);
StageState create_right_branch_matrix(cost_matrix_t m, vertex_t v, cost_t lb);
tsp_solutions_t filter_solutions(tsp_solutions_t solutions);

tsp_solutions_t solve_tsp(const cost_matrix_t& cm);

#endif //IMPLEMENTATION_TSP_HPP
